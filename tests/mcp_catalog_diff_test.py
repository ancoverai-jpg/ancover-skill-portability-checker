import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/mcp-tool-catalog-diff/scripts/compare.py"
spec = importlib.util.spec_from_file_location("catalog", SCRIPT)
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


def sample():
    return {"profile": catalog.PROFILE, "serverKey": "synthetic-server",
            "complete": True, "tools": [{"name": "sample_read", "description": "Read sample",
                "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}},
                "annotations": {"readOnlyHint": True}}]}


def parsed(value):
    return catalog.decode(json.dumps(value).encode())


def compare(left, right):
    return catalog.compare(parsed(left), parsed(right))


class CatalogDiffTests(unittest.TestCase):
    def test_key_tool_order_and_capture_metadata_do_not_create_changes(self):
        left = sample()
        left["tools"].append({"name": "other", "inputSchema": {"properties": {}, "type": "object"}})
        right = json.loads(json.dumps(left, sort_keys=True))
        right["tools"].reverse()
        right["capturedAt"] = "different operator metadata"
        self.assertEqual(compare(left, right)["status"], "UNCHANGED")

    def test_same_name_description_change_requires_review(self):
        left, right = sample(), sample()
        right["tools"][0]["description"] = "Different behavior declaration"
        report = compare(left, right)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertEqual(report["changes"][0]["fields"], ["description"])

    def test_same_name_input_schema_change_is_visible(self):
        left, right = sample(), sample()
        right["tools"][0]["inputSchema"]["required"] = ["query"]
        self.assertEqual(compare(left, right)["changes"][0]["fields"], ["inputSchema"])

    def test_known_unknown_and_absent_null_fields_are_included(self):
        for field in ["title", "outputSchema", "annotations", "vendorSecret"]:
            left, right = sample(), sample()
            left["tools"][0].pop(field, None)
            right["tools"][0][field] = None
            category = field if field in catalog.FIELDS else "other"
            self.assertIn(category, compare(left, right)["changes"][0]["fields"])

    def test_rename_is_removed_plus_added_with_original_indices(self):
        left, right = sample(), sample()
        right["tools"][0]["name"] = "renamed"
        report = compare(left, right)
        self.assertEqual(report["counts"], {"added": 1, "removed": 1, "modified": 0})
        self.assertEqual(len(report["changes"]), 2)
        self.assertEqual({x["toolId"] for x in report["changes"]}, {
            hashlib.sha256(n.encode()).hexdigest() for n in ["sample_read", "renamed"]})

    def test_array_order_is_preserved_conservatively(self):
        left, right = sample(), sample()
        left["tools"][0]["inputSchema"]["required"] = ["a", "b"]
        right["tools"][0]["inputSchema"]["required"] = ["b", "a"]
        self.assertEqual(compare(left, right)["status"], "REVIEW_REQUIRED")

    def test_numeric_precision_and_spelling_do_not_collapse(self):
        left, right = sample(), sample()
        left["tools"][0]["inputSchema"]["maximum"] = 9007199254740992
        right["tools"][0]["inputSchema"]["maximum"] = 9007199254740993
        self.assertEqual(compare(left, right)["status"], "REVIEW_REQUIRED")
        base = json.dumps(left).replace("9007199254740992", "1")
        for number in ["1.0", "1e0", "-0"]:
            changed = base.replace('"maximum": 1', '"maximum": ' + number)
            self.assertEqual(catalog.compare(catalog.decode(base.encode()),
                                            catalog.decode(changed.encode()))["status"],
                             "REVIEW_REQUIRED")

    def test_duplicate_json_keys_are_not_silently_overwritten(self):
        with self.assertRaisesRegex(catalog.ReviewError, "DUPLICATE_JSON_KEY"):
            catalog.decode(b'{"x":1,"x":2}')

    def test_duplicate_tool_names_are_unknown_even_when_identical(self):
        data = sample()
        data["tools"].append(copy.deepcopy(data["tools"][0]))
        with self.assertRaisesRegex(catalog.ReviewError, "DUPLICATE_TOOL_NAME"):
            compare(data, data)

    def test_scope_profile_and_partial_capture_fail_closed(self):
        variants = []
        for key, value in [("serverKey", "different"), ("profile", "wrong"),
                           ("complete", False), ("complete", "true"), ("nextCursor", None)]:
            data = sample()
            data[key] = value
            variants.append(data)
        for data in variants:
            with self.subTest(data=data), self.assertRaises(catalog.ReviewError):
                compare(sample(), data)

    def test_tool_and_catalog_shape_limits(self):
        cases = [None, {}, {"name": ""}, {"name": "x", "inputSchema": True}]
        for tool in cases:
            data = sample()
            data["tools"] = [tool]
            with self.subTest(tool=tool), self.assertRaises(catalog.ReviewError):
                compare(data, data)
        data = sample()
        data["tools"] = [{"name": str(i), "inputSchema": {}} for i in range(257)]
        with self.assertRaisesRegex(catalog.ReviewError, "TOOLS_LIST_LIMIT"):
            compare(data, data)

    def test_strict_json_numeric_and_structure_limits(self):
        for raw in [b"\xff", b"{bad", b'{"x":NaN}', ("[" * 50 + "0" + "]" * 50).encode(),
                    json.dumps([0] * 12001).encode(), b"1" * 129]:
            with self.subTest(size=len(raw)), self.assertRaises(catalog.ReviewError):
                catalog.decode(raw)

    def test_real_cli_is_read_only_and_omits_private_values_and_names(self):
        with tempfile.TemporaryDirectory() as directory:
            left, right = sample(), sample()
            right["tools"][0]["description"] = "SENTINEL_PRIVATE_DESCRIPTION"
            right["tools"][0]["vendorSecret"] = "SENTINEL_PRIVATE_FIELD"
            a, b = Path(directory) / "a.json", Path(directory) / "b.json"
            a.write_text(json.dumps(left), encoding="utf-8")
            b.write_text(json.dumps(right), encoding="utf-8")
            before = (a.read_bytes(), b.read_bytes())
            result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), str(a), str(b)],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(before, (a.read_bytes(), b.read_bytes()))
            for private in ["SENTINEL", "vendorSecret", "sample_read", directory]:
                self.assertNotIn(private, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["changes"][0]["beforeIndex"], 0)

    def test_actual_cli_unchanged_and_invalid_usage_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            selected = Path(directory) / "catalog.json"
            selected.write_text(json.dumps(sample()), encoding="utf-8")
            for args, expected in [([str(selected), str(selected)], 0), ([], 2),
                                   ([directory, str(selected)], 2),
                                   ([str(selected) + ".missing", str(selected)], 2)]:
                result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), *args],
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, expected)
                json.loads(result.stdout)

    def test_file_size_is_bounded_in_actual_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            selected = Path(directory) / "oversize.json"
            selected.write_bytes(b" " * (catalog.MAX_BYTES + 1))
            result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT),
                                     str(selected), str(selected)], capture_output=True,
                                    text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["reason"], "FILE_SIZE_LIMIT")

    def test_empty_complete_catalogs_are_selected_data_not_live_health(self):
        data = sample()
        data["tools"] = []
        result = compare(data, data)
        self.assertEqual(result["status"], "UNCHANGED")
        self.assertEqual(result["beforeCount"], 0)
        self.assertFalse(result["liveCalls"])
        self.assertEqual(result["serverIdentity"], "OPERATOR_ASSERTION")


if __name__ == "__main__":
    unittest.main()
