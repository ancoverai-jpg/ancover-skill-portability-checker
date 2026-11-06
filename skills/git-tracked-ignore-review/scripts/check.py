#!/usr/bin/env python3
"""Report index entries matching the selected repository's .gitignore rules."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

PROFILE = "ancover-git-tracked-ignore-v1"
GIT_TIMEOUT = 10
MAX_OUTPUT_BYTES = 1024 * 1024
SELECTION_OVERRIDES = (
    "GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
    "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT",
)


class InspectionError(ValueError):
    """A fixed reason code suitable for the public report."""


def run_git(git, root, environment, *arguments):
    try:
        completed = subprocess.run(
            [git, "-c", "core.fsmonitor=false", "-C", str(root), *arguments],
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=GIT_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise InspectionError("GIT_TIMEOUT") from None
    except OSError:
        raise InspectionError("GIT_UNAVAILABLE") from None

    if completed.returncode != 0 or completed.stderr:
        raise InspectionError("GIT_DIAGNOSTIC")
    if len(completed.stdout) > MAX_OUTPUT_BYTES:
        raise InspectionError("GIT_OUTPUT_LIMIT")
    return completed.stdout


def inspect(directory):
    if any(os.environ.get(key) for key in SELECTION_OVERRIDES):
        raise InspectionError("GIT_SELECTION_OVERRIDE")

    root = Path(directory).resolve(strict=True)
    if not root.is_dir():
        raise InspectionError("REPOSITORY_DIRECTORY_REQUIRED")
    git = shutil.which("git")
    if git is None:
        raise InspectionError("GIT_UNAVAILABLE")

    environment = {
        **os.environ,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_NO_LAZY_FETCH": "1",
    }
    location = run_git(
        git, root, environment, "rev-parse", "--is-inside-work-tree", "--show-prefix"
    )
    if location.splitlines() != [b"true", b""]:
        raise InspectionError("WORKTREE_ROOT_REQUIRED")

    raw = run_git(
        git, root, environment, "ls-files", "--cached", "--ignored", "-z",
        "--exclude-per-directory=.gitignore",
    )
    if raw and not raw.endswith(b"\0"):
        raise InspectionError("UNEXPECTED_GIT_OUTPUT")

    paths = sorted(set(raw.split(b"\0")) - {b""})
    digest = hashlib.sha256(b"".join(path + b"\0" for path in paths)).hexdigest()
    return {
        "profile": PROFILE,
        "status": "INDEX_MATCHES" if paths else "NO_INDEX_MATCHES",
        "ruleScope": "REPOSITORY_GITIGNORE",
        "matchedPathCount": len(paths),
        "matchedPathsSha256": digest,
    }


def main(arguments):
    try:
        if len(arguments) != 1 or not arguments[0]:
            raise InspectionError("USAGE_WORKTREE_ROOT_REQUIRED")
        report = inspect(arguments[0])
    except InspectionError as error:
        report = {"profile": PROFILE, "status": "INDETERMINATE", "reason": str(error)}
    except (OSError, RuntimeError, ValueError):
        report = {
            "profile": PROFILE,
            "status": "INDETERMINATE",
            "reason": "REPOSITORY_ACCESS_UNRESOLVED",
        }

    print(json.dumps(report, separators=(",", ":")))
    return {"NO_INDEX_MATCHES": 0, "INDEX_MATCHES": 1, "INDETERMINATE": 2}[
        report["status"]
    ]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
