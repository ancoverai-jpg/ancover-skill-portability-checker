#!/usr/bin/env python3
"""Compare two selected MCP-style tool catalogs without contacting servers."""
import hashlib
import json
import os
import stat
import sys

PROFILE = "ancover-mcp-tool-catalog-v1"
MAX_BYTES = 1024 * 1024
MAX_TOOLS = 256
MAX_NODES = 12000
MAX_DEPTH = 48
FIELDS = ("description", "title", "inputSchema", "outputSchema", "annotations")


class ReviewError(ValueError):
    pass


class Number:
    """Preserve number lexemes instead of silently rounding large JSON numbers."""
    def __init__(self, text):
        if len(text) > 128:
            raise ReviewError("NUMBER_LEXEME_LIMIT")
        self.text = text


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ReviewError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def constant(_):
    raise ReviewError("NON_JSON_CONSTANT")


def decode(raw):
    if len(raw) > MAX_BYTES:
        raise ReviewError("FILE_SIZE_LIMIT")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_int=Number, parse_float=Number,
                          parse_constant=constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise ReviewError("INVALID_JSON") from None
    pending, count = [(data, 0)], 0
    while pending:
        value, depth = pending.pop()
        count += 1
        if depth > MAX_DEPTH or count > MAX_NODES:
            raise ReviewError("STRUCTURE_LIMIT")
        if isinstance(value, dict):
            pending.extend((v, depth + 1) for v in value.values())
        elif isinstance(value, list):
            pending.extend((v, depth + 1) for v in value)
    return data


def tagged(value):
    # Application-specific typed representation; NOT RFC8785/JCS or semantic JSON Schema.
    if isinstance(value, Number):
        return ["number", value.text]
    if value is None:
        return ["null"]
    if isinstance(value, bool):
        return ["boolean", value]
    if isinstance(value, str):
        return ["string", value]
    if isinstance(value, list):
        return ["array", [tagged(v) for v in value]]
    if isinstance(value, dict):
        return ["object", [[k, tagged(value[k])] for k in sorted(value)]]
    raise ReviewError("UNSUPPORTED_VALUE")


def digest(value):
    raw = json.dumps(tagged(value), ensure_ascii=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def validate(data):
    if not isinstance(data, dict) or data.get("profile") != PROFILE:
        raise ReviewError("PROFILE_REQUIRED")
    scope = data.get("serverKey")
    if not isinstance(scope, str) or not scope or len(scope) > 128:
        raise ReviewError("SERVER_KEY_REQUIRED")
    if data.get("complete") is not True or "nextCursor" in data:
        raise ReviewError("COMPLETE_CATALOG_REQUIRED")
    tools = data.get("tools")
    if not isinstance(tools, list) or len(tools) > MAX_TOOLS:
        raise ReviewError("TOOLS_LIST_LIMIT")
    indexed = {}
    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            raise ReviewError("TOOL_OBJECT_REQUIRED")
        name = tool.get("name")
        if not isinstance(name, str) or not name or len(name) > 256:
            raise ReviewError("TOOL_NAME_REQUIRED")
        if name in indexed:
            raise ReviewError("DUPLICATE_TOOL_NAME")
        if not isinstance(tool.get("inputSchema"), dict):
            raise ReviewError("INPUT_SCHEMA_OBJECT_REQUIRED")
        indexed[name] = (index, tool)
    return scope, indexed


def compare(before, after):
    scope_a, tools_a = validate(before)
    scope_b, tools_b = validate(after)
    if scope_a != scope_b:
        raise ReviewError("SERVER_SCOPE_MISMATCH")
    changes = []
    counts = {"added": 0, "removed": 0, "modified": 0}
    for name in sorted(set(tools_a) | set(tools_b)):
        left, right = tools_a.get(name), tools_b.get(name)
        identity = hashlib.sha256(name.encode("utf-8")).hexdigest()
        item = {"toolId": identity, "beforeIndex": left[0] if left else None,
                "afterIndex": right[0] if right else None}
        if not left:
            counts["added"] += 1
            changes.append({**item, "change": "ADDED"})
        elif not right:
            counts["removed"] += 1
            changes.append({**item, "change": "REMOVED"})
        elif digest(left[1]) != digest(right[1]):
            fields = []
            for field in FIELDS:
                if (field in left[1]) != (field in right[1]) or (
                    field in left[1] and digest(left[1][field]) != digest(right[1][field])
                ):
                    fields.append(field)
            extra_a = {k: v for k, v in left[1].items() if k not in FIELDS and k != "name"}
            extra_b = {k: v for k, v in right[1].items() if k not in FIELDS and k != "name"}
            if digest(extra_a) != digest(extra_b):
                fields.append("other")
            counts["modified"] += 1
            changes.append({**item, "change": "MODIFIED", "fields": fields})
    return {"profile": PROFILE, "status": "REVIEW_REQUIRED" if changes else "UNCHANGED",
            "counts": counts, "beforeCount": len(tools_a), "afterCount": len(tools_b),
            "changes": changes, "semanticCompatibility": "NOT_ASSESSED",
            "serverIdentity": "OPERATOR_ASSERTION", "liveCalls": False}


def read_selected(path):
    if not stat.S_ISREG(os.stat(path).st_mode):
        raise ReviewError("REGULAR_FILE_REQUIRED")
    with open(path, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ReviewError("REGULAR_FILE_REQUIRED")
        raw = stream.read(MAX_BYTES + 1)
    return decode(raw), hashlib.sha256(raw).hexdigest()


def main(args):
    try:
        if len(args) != 2:
            raise ReviewError("USAGE_BEFORE_AFTER_JSON")
        before, hash_a = read_selected(args[0])
        after, hash_b = read_selected(args[1])
        answer = {**compare(before, after), "beforeSnapshotSha256": hash_a,
                  "afterSnapshotSha256": hash_b}
    except ReviewError as error:
        answer = {"profile": PROFILE, "status": "INDETERMINATE", "reason": str(error)}
    except Exception:
        # Never expose raw data, tool names, paths or library exception messages.
        answer = {"profile": PROFILE, "status": "INDETERMINATE",
                  "reason": "INPUT_OR_PROFILE_UNRESOLVED"}
    print(json.dumps(answer, ensure_ascii=True, separators=(",", ":")))
    return {"UNCHANGED": 0, "REVIEW_REQUIRED": 1, "INDETERMINATE": 2}[answer["status"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
