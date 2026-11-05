#!/usr/bin/env python3
"""Offline, bounded review of one selected legacy MCP structured result."""
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import subprocess
import sys

PROFILE = "mcp-2025-06-18-draft202012"
DIALECT = "https://json-schema.org/draft/2020-12/schema"
MAX_BYTES = 1024 * 1024
MAX_NODES = 12000
MAX_DEPTH = 48
TIMEOUT = 5


def report(status, reason, **extra):
    return {"profile": PROFILE, "status": status, "reason": reason,
            "formatAssertions": False, "transportTested": False, **extra}


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("non-json number")


def decode(raw):
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=reject_constant)
    pending = [(data, 0)]
    count = 0
    while pending:
        node, depth = pending.pop()
        count += 1
        if count > MAX_NODES or depth > MAX_DEPTH:
            raise ValueError("limit")
        if isinstance(node, float) and not math.isfinite(node):
            raise ValueError("numeric range")
        if isinstance(node, dict):
            pending.extend((v, depth + 1) for v in node.values())
        elif isinstance(node, list):
            pending.extend((v, depth + 1) for v in node)
    return data


def evaluate(data):
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
    from referencing import Registry
    from referencing.exceptions import NoSuchResource

    if not isinstance(data, dict) or data.get("profile") != PROFILE:
        return report("INDETERMINATE", "INPUT_PROFILE")
    tool, result = data.get("tool"), data.get("callResult")
    if not isinstance(tool, dict) or not isinstance(result, dict):
        return report("INDETERMINATE", "SELECTED_OBJECTS_REQUIRED")
    if "isError" in result and type(result["isError"]) is not bool:
        return report("INDETERMINATE", "INVALID_ERROR_FLAG")
    if result.get("isError") is True:
        return report("TOOL_ERROR", "TOOL_REPORTED_FAILURE")
    if "outputSchema" not in tool:
        return report("NOT_APPLICABLE", "NO_OUTPUT_SCHEMA")
    schema = tool["outputSchema"]
    if not isinstance(schema, dict) or schema.get("type") != "object":
        return report("INDETERMINATE", "OBJECT_SCHEMA_PROFILE_REQUIRED")
    # This conservative scan may also reject keywords in annotation/const data.
    pending = [schema]
    while pending:
        node = pending.pop()
        if isinstance(node, dict):
            if "$schema" in node and node["$schema"] != DIALECT:
                return report("INDETERMINATE", "UNSUPPORTED_DIALECT")
            if "$vocabulary" in node:
                return report("INDETERMINATE", "VOCABULARY_PROFILE_UNSUPPORTED")
            for key in ("$ref", "$dynamicRef"):
                if key in node and (not isinstance(node[key], str)
                                    or not node[key].startswith("#")):
                    return report("INDETERMINATE", "NONLOCAL_REFERENCE")
            pending.extend(node.values())
        elif isinstance(node, list):
            pending.extend(node)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        return report("INDETERMINATE", "INVALID_SCHEMA")
    if not isinstance(result.get("structuredContent"), dict):
        return report("MISMATCH", "STRUCTURED_OBJECT_MISSING")
    # No network or filesystem reference retrieval, including through $id.
    def deny(uri):
        raise NoSuchResource(ref=uri)
    validator = Draft202012Validator(schema, registry=Registry(retrieve=deny))
    # Stop on the first mismatch; do not emit instance values, paths or messages.
    error = next(validator.iter_errors(result["structuredContent"]), None)
    if error is not None:
        return report("MISMATCH", "SCHEMA_CONSTRAINT")
    return report("MATCH", "SELECTED_STRUCTURED_CONTENT_ONLY")


def run(raw, timeout=TIMEOUT):
    digest = hashlib.sha256(raw).hexdigest()
    try:
        decode(raw)
    except (ValueError, UnicodeError, RecursionError):
        return report("INDETERMINATE", "INVALID_OR_EXCESSIVE_JSON",
                      snapshotSha256=digest)
    command = [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--worker"]
    try:
        child = subprocess.run(command, input=raw, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, timeout=timeout,
                               check=False)
        if child.returncode != 0 or len(child.stdout) > 2048:
            raise ValueError("worker")
        answer = json.loads(child.stdout)
        if answer.get("status") not in {
                "MATCH", "MISMATCH", "TOOL_ERROR", "NOT_APPLICABLE", "INDETERMINATE"}:
            raise ValueError("worker result")
    except subprocess.TimeoutExpired:
        answer = report("INDETERMINATE", "WORKER_TIMEOUT")
    except (OSError, ValueError, TypeError):
        answer = report("INDETERMINATE", "WORKER_UNAVAILABLE")
    return {**answer, "snapshotSha256": digest}


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--worker":
        try:
            raw = sys.stdin.buffer.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise ValueError("size")
            answer = evaluate(decode(raw))
        except ImportError:
            answer = report("INDETERMINATE", "DEPENDENCIES_UNAVAILABLE")
        except Exception:
            # Deliberately hide library exception text: it can contain payloads.
            answer = report("INDETERMINATE", "VALIDATION_UNRESOLVED")
        print(json.dumps(answer, separators=(",", ":")))
        return 0
    if len(sys.argv) != 2:
        answer = report("INDETERMINATE", "USAGE_SNAPSHOT_JSON")
    else:
        try:
            if not stat.S_ISREG(os.stat(sys.argv[1]).st_mode):
                raise ValueError("regular file")
            with open(sys.argv[1], "rb") as selected:
                if not stat.S_ISREG(os.fstat(selected.fileno()).st_mode):
                    raise ValueError("regular file")
                raw = selected.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                answer = report("INDETERMINATE", "SNAPSHOT_TOO_LARGE")
            else:
                answer = run(raw)
        except (OSError, ValueError):
            answer = report("INDETERMINATE", "SNAPSHOT_UNREADABLE")
    print(json.dumps(answer, separators=(",", ":")))
    return 0 if answer["status"] == "MATCH" else (
        1 if answer["status"] in {"MISMATCH", "TOOL_ERROR"} else 2)


if __name__ == "__main__":
    sys.exit(main())
