import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/mcp-structured-result-check/scripts/check.py"
spec = importlib.util.spec_from_file_location("mcp_check", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
BASE = {
    "profile": check.PROFILE,
    "tool": {"outputSchema": {"type": "object", "properties": {
        "count": {"type": "integer", "minimum": 0}},
        "required": ["count"], "additionalProperties": False}},
    "callResult": {"content": [{"type": "text", "text": "unrelated"}],
                   "structuredContent": {"count": 2}, "isError": False}
}


class StructuredResultTests(unittest.TestCase):
    def sample(self):
        return copy.deepcopy(BASE)

    def status(self, data):
        return check.evaluate(data)["status"]

    def test_correct_payload_ignores_envelope_siblings(self):
        self.assertEqual(self.status(self.sample()), "MATCH")

    def test_wrong_type_required_extra_and_numeric_constraint(self):
        for value in [{"count": "2"}, {}, {"count": 2, "extra": True}, {"count": -1}]:
            with self.subTest(value=value):
                data = self.sample()
                data["callResult"]["structuredContent"] = value
                self.assertEqual(self.status(data), "MISMATCH")

    def test_text_json_is_never_a_substitute(self):
        data = self.sample()
        del data["callResult"]["structuredContent"]
        data["callResult"]["content"][0]["text"] = '{"count":2}'
        self.assertEqual(self.status(data), "MISMATCH")

    def test_null_and_array_are_not_structured_objects(self):
        for value in [None, [], "{}", 5, True]:
            data = self.sample()
            data["callResult"]["structuredContent"] = value
            self.assertEqual(self.status(data), "MISMATCH")

    def test_error_cannot_pass_even_with_matching_payload(self):
        data = self.sample()
        data["callResult"]["isError"] = True
        self.assertEqual(self.status(data), "TOOL_ERROR")

    def test_error_flag_type_is_checked(self):
        data = self.sample()
        data["callResult"]["isError"] = "false"
        self.assertEqual(self.status(data), "INDETERMINATE")

    def test_no_schema_is_not_applicable(self):
        data = self.sample()
        data["tool"] = {}
        self.assertEqual(self.status(data), "NOT_APPLICABLE")

    def test_schema_dialect_and_bad_schema_are_unknown(self):
        for schema in [{"type": "array"}, {"type": "object", "required": 2},
                       {"type": "object", "$schema": "http://json-schema.org/draft-07/schema#"},
                       {"type": "object", "$vocabulary": {}}]:
            data = self.sample()
            data["tool"]["outputSchema"] = schema
            self.assertEqual(self.status(data), "INDETERMINATE")

    def test_remote_and_file_refs_never_retrieve(self):
        for ref in ["https://example.invalid/schema", "file:///private/schema", "urn:other"]:
            data = self.sample()
            data["tool"]["outputSchema"]["$ref"] = ref
            self.assertEqual(check.evaluate(data)["reason"], "NONLOCAL_REFERENCE")

    def test_local_refs_composition_and_array_constraints(self):
        data = self.sample()
        data["tool"]["outputSchema"] = {
            "type": "object", "$defs": {"items": {"type": "array",
                "items": {"type": "integer"}, "minItems": 1}},
            "properties": {"values": {"$ref": "#/$defs/items"}},
            "required": ["values"], "allOf": [{"maxProperties": 1}]}
        data["callResult"]["structuredContent"] = {"values": [3]}
        self.assertEqual(self.status(data), "MATCH")
        data["callResult"]["structuredContent"] = {"values": ["bad"]}
        self.assertEqual(self.status(data), "MISMATCH")

    def test_format_is_annotation_and_empty_object_is_valid(self):
        data = self.sample()
        data["tool"]["outputSchema"] = {
            "type": "object", "properties": {"email": {"type": "string", "format": "email"}}}
        data["callResult"]["structuredContent"] = {"email": "not-an-email"}
        self.assertEqual(self.status(data), "MATCH")
        data["callResult"]["structuredContent"] = {}
        self.assertEqual(self.status(data), "MATCH")

    def test_json_strictness_and_depth(self):
        for raw in [b'{"x":1,"x":2}', b'{"x":NaN}', b'{bad', b'\xff', b'{"x":1e999}',
                    ("[" * 50 + "0" + "]" * 50).encode()]:
            self.assertEqual(check.run(raw)["status"], "INDETERMINATE")

    def test_node_bound(self):
        raw = json.dumps([0] * 12001).encode()
        self.assertEqual(check.run(raw)["reason"], "INVALID_OR_EXCESSIVE_JSON")

    def test_worker_timeout_fails_closed(self):
        result = check.run(json.dumps(BASE).encode(), timeout=0.000001)
        self.assertEqual(result["reason"], "WORKER_TIMEOUT")

    def test_real_cli_sample_and_report_no_payload_values(self):
        data = self.sample()
        data["callResult"]["structuredContent"] = {"secret-field": "SENTINEL_DO_NOT_PRINT"}
        with tempfile.TemporaryDirectory() as directory:
            selected = Path(directory) / "snapshot.json"
            selected.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), str(selected)],
                                    capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("SENTINEL", result.stdout + result.stderr)
        self.assertNotIn("secret-field", result.stdout + result.stderr)
        self.assertIn("snapshotSha256", json.loads(result.stdout))

    def test_real_cli_missing_oversize_and_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            selected = Path(directory) / "large.json"
            selected.write_bytes(b" " * (check.MAX_BYTES + 1))
            for args in [[str(selected)], [str(selected) + ".missing"], [directory], []]:
                result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), *args],
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["status"], "INDETERMINATE")


if __name__ == "__main__":
    unittest.main()
