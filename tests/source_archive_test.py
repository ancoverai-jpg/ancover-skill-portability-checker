import importlib.util
import io
import json
import stat
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/source-archive-review/scripts/check.py"
spec = importlib.util.spec_from_file_location("archive_checker", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

def policy():
    return {"schemaVersion": 1, "sourceRevision": "a" * 40, "rootPrefix": "repo/", "requiredFiles": ["README.md"], "requiredPrefixes": []}

def archive(entries, compression=zipfile.ZIP_DEFLATED):
    out = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(out, "w", compression) as source:
            for name, value in entries:
                if isinstance(name, str):
                    member = zipfile.ZipInfo(name)
                    member.filename = name
                    member.orig_filename = name
                    member.compress_type = compression
                    source.writestr(member, value)
                else:
                    source.writestr(name, value)
    return out.getvalue()

def kinds(result):
    return {x["kind"] for x in result["findings"]}

class ArchiveReviewTests(unittest.TestCase):
    def test_valid_archive_and_fingerprint(self):
        data = archive([("repo/README.md", "hello")])
        result = checker.inspect(policy(), data)
        self.assertTrue(result["configuredChecksSatisfied"])
        self.assertEqual(len(result["archiveSha256"]), 64)
        self.assertEqual(result["evidence"], "ZIP_METADATA_AND_SMALL_ENTRY_INSPECTION")

    def test_missing_exact_file(self):
        self.assertIn("MISSING_FILE", kinds(checker.inspect(policy(), archive([]))))

    def test_empty_required_prefix_including_directory_only(self):
        p = policy()
        p["requiredPrefixes"] = ["vendor/library/"]
        data = archive([("repo/README.md", "ok"), ("repo/vendor/library/", "")])
        self.assertIn("EMPTY_REQUIRED_PREFIX", kinds(checker.inspect(p, data)))

    def test_nonempty_prefix_is_only_presence_not_completeness(self):
        p = policy()
        p["requiredPrefixes"] = ["vendor/library/"]
        data = archive([("repo/README.md", "ok"), ("repo/vendor/library/.gitkeep", "")])
        self.assertTrue(checker.inspect(p, data)["configuredChecksSatisfied"])

    def test_lfs_pointer_exact_and_normal_text(self):
        pointer = "version https://git-lfs.github.com/spec/v1\noid sha256:" + "a" * 64 + "\nsize 200\n"
        data = archive([("repo/README.md", "ok"), ("repo/asset.bin", pointer)])
        self.assertIn("CANONICAL_LFS_POINTER", kinds(checker.inspect(policy(), data)))
        self.assertNotIn("CANONICAL_LFS_POINTER", kinds(checker.inspect(policy(), archive([("repo/README.md", "example:\n" + pointer)]))))

    def test_traversal_and_absolute_names_do_not_leak_contents(self):
        for name in ("../escape", "/absolute", "C:/drive", "repo\\file", "repo/./file"):
            result = checker.inspect(policy(), archive([("repo/README.md", "ok"), (name, "SENTINEL_PRIVATE")]))
            self.assertIn("UNSAFE_MEMBER_NAME", kinds(result))
            self.assertNotIn("SENTINEL_PRIVATE", json.dumps(result))

    def test_duplicates_and_case_collisions(self):
        data = archive([("repo/README.md", "a"), ("repo/README.md", "b"), ("repo/readme.md", "c")])
        self.assertEqual(kinds(checker.inspect(policy(), data)), {"DUPLICATE_MEMBER", "CASE_COLLISION"})

    def test_symlink_metadata_is_not_regular_source(self):
        link = zipfile.ZipInfo("repo/README.md")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        result = checker.inspect(policy(), archive([(link, "/outside")]))
        self.assertIn("SYMLINK_METADATA", kinds(result))
        self.assertIn("MISSING_FILE", kinds(result))

    def test_policy_schema_types_and_duplicates(self):
        changes = [
            lambda p: p.update(schemaVersion=True),
            lambda p: p.update(sourceRevision="main"),
            lambda p: p.update(rootPrefix="../"),
            lambda p: p.update(requiredFiles=[]),
            lambda p: p.update(requiredFiles=["a", "a"]),
            lambda p: p.update(requiredFiles=["a/"]),
            lambda p: p.update(requiredPrefixes=["vendor"]),
            lambda p: p.update(extra="SENTINEL"),
        ]
        for change in changes:
            p = policy()
            change(p)
            with self.assertRaises(ValueError):
                checker.validate(p)

    def test_bounds_and_unsupported_compression(self):
        with self.assertRaises(ValueError):
            checker.inspect(policy(), b"x" * (checker.MAX_ZIP + 1))
        with self.assertRaises(ValueError):
            checker.inspect(policy(), archive([("repo/README.md", "ok")], zipfile.ZIP_BZIP2))
        with self.assertRaises(ValueError):
            checker.inspect(policy(), archive([(f"f{i}", "") for i in range(10001)]))

    def test_large_entry_prefix_is_not_a_full_content_scan(self):
        pointer = b"version https://git-lfs.github.com/spec/v1\n" + b"x" * 2000
        result = checker.inspect(policy(), archive([("repo/README.md", pointer)]))
        self.assertTrue(result["configuredChecksSatisfied"])

    def test_real_cli_input_preservation_and_fixed_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = root / "policy.json"
            source = root / "source.zip"
            data = archive([("repo/README.md", "ok"), ("../escape.txt", "SYNTHETIC_SECRET")])
            manifest.write_text(json.dumps(policy()), encoding="utf-8")
            source.write_bytes(data)
            run = lambda: subprocess.run([sys.executable, "-B", str(SCRIPT), str(manifest), str(source)], capture_output=True, text=True)
            result = run()
            self.assertEqual(result.returncode, 1)
            self.assertFalse((root / "escape.txt").exists())
            self.assertEqual(source.read_bytes(), data)
            self.assertNotIn("SYNTHETIC_SECRET", result.stdout + result.stderr)
            source.write_bytes(archive([("repo/README.md", "ok")]))
            self.assertEqual(run().returncode, 0)
            for bad in (b"{SYNTHETIC_SECRET", b"\xff", b'{"schemaVersion":1,"schemaVersion":1}', b"x" * (checker.MAX_MANIFEST + 1)):
                manifest.write_bytes(bad)
                result = run()
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr.strip(), '{"error": "INVALID_INPUT"}')
            manifest.write_text(json.dumps(policy()), encoding="utf-8")
            source.write_bytes(b"not zip")
            self.assertEqual(run().returncode, 2)
            self.assertEqual(checker.main([])[0], 2)
            self.assertEqual(checker.main(["--help"])[0], 0)

if __name__ == "__main__":
    unittest.main()
