import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/git-tracked-ignore-review/scripts/check.py"


class GitTrackedIgnoreReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "selected repository"
        self.root.mkdir()
        self.environment = {
            **os.environ,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
        }
        self.git("init", "--quiet", "--template=")

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "core.autocrlf=false", "-C", str(self.root), *args],
            env=self.environment, capture_output=True, check=True, timeout=10,
        ).stdout

    def file(self, path, text="synthetic fixture\n"):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def review(self, *args, environment=None):
        result = subprocess.run(
            [sys.executable, "-I", "-B", str(SCRIPT), *map(str, args)],
            env=environment or self.environment,
            capture_output=True, text=True, timeout=25,
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout), result.stdout

    def test_indexed_ignore_match_and_untracked_exclusion(self):
        tracked = "synthetic tracked.log"
        self.file(tracked, "SENTINEL_PRIVATE_CONTENT\n")
        self.git("add", "--", tracked)
        self.file("untracked.log")
        self.file(".gitignore", "*.log\n")
        index = self.root / ".git/index"
        before = index.read_bytes()
        contents = (self.root / tracked).read_bytes()

        code, report, stdout = self.review(self.root)

        self.assertEqual(code, 1)
        self.assertEqual(report["status"], "INDEX_MATCHES")
        self.assertEqual(report["matchedPathCount"], 1)
        self.assertEqual(report["matchedPathsSha256"],
                         hashlib.sha256(b"synthetic tracked.log\0").hexdigest())
        for value in (tracked, "untracked.log", "SENTINEL", str(self.root)):
            self.assertNotIn(value, stdout)
        self.assertEqual(index.read_bytes(), before)
        self.assertEqual((self.root / tracked).read_bytes(), contents)

    def test_nested_rules_and_negation_use_git_semantics(self):
        self.file("nested/private.log")
        self.file("nested/keep.log")
        self.file("other.log")
        self.git("add", "--", "nested/private.log", "nested/keep.log", "other.log")
        self.file("nested/.gitignore", "*.log\n!keep.log\n")

        code, report, _ = self.review(self.root)

        self.assertEqual(code, 1)
        self.assertEqual(report["matchedPathCount"], 1)
        self.assertEqual(report["matchedPathsSha256"],
                         hashlib.sha256(b"nested/private.log\0").hexdigest())

    def test_local_and_global_excludes_are_outside_repository_profile(self):
        self.file("local.dat")
        self.file("machine.dat")
        self.git("add", "--", "local.dat", "machine.dat")
        self.file(".git/info/exclude", "local.dat\n")
        self.file("global-rules", "machine.dat\n")
        self.git("config", "core.excludesFile", str(self.root / "global-rules"))
        effective = self.git("ls-files", "-ci", "-z", "--exclude-standard")
        self.assertEqual(set(effective.split(b"\0")) - {b""},
                         {b"local.dat", b"machine.dat"})

        code, report, _ = self.review(self.root)

        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "NO_INDEX_MATCHES")
        self.assertEqual(report["matchedPathCount"], 0)

    def test_worktree_rule_change_is_visible_before_staging(self):
        self.file("sample.dat")
        self.file(".gitignore", "")
        self.git("add", "--", "sample.dat", ".gitignore")
        self.assertEqual(self.review(self.root)[0], 0)
        self.file(".gitignore", "sample.dat\n")
        self.assertEqual(self.review(self.root)[0], 1)

    def test_invalid_inputs_and_subdirectory_are_indeterminate(self):
        self.file("child/file")
        for arguments in ((), (self.root, self.root), (self.root / "missing",),
                          (self.root / "child/file",), (self.root / "child",),
                          (Path(self.temporary.name),)):
            with self.subTest(argument_count=len(arguments)):
                code, report, stdout = self.review(*arguments)
                self.assertEqual(code, 2)
                self.assertEqual(report["status"], "INDETERMINATE")
                self.assertNotIn(str(self.root), stdout)

    def test_index_override_is_indeterminate(self):
        code, report, stdout = self.review(
            self.root, environment={**self.environment, "GIT_INDEX_FILE": "private-index"}
        )
        self.assertEqual(code, 2)
        self.assertEqual(report["reason"], "GIT_SELECTION_OVERRIDE")
        self.assertNotIn("private-index", stdout)

    def test_bare_repository_is_indeterminate(self):
        bare = Path(self.temporary.name) / "bare"
        subprocess.run(["git", "init", "--quiet", "--bare", "--template=", str(bare)],
                       env=self.environment, capture_output=True, check=True, timeout=10)
        code, report, _ = self.review(bare)
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "INDETERMINATE")

    def test_missing_git_is_indeterminate(self):
        code, report, _ = self.review(
            self.root, environment={**self.environment, "PATH": str(self.root)}
        )
        self.assertEqual(code, 2)
        self.assertEqual(report["reason"], "GIT_UNAVAILABLE")


if __name__ == "__main__":
    unittest.main()
