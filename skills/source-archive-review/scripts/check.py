"""Offline, non-extracting source ZIP review. Python 3.10+; standard library only."""
import hashlib
import io
import json
import re
import stat
import sys
import zipfile
from pathlib import Path

MAX_ZIP = 16 * 1024 * 1024
MAX_MANIFEST = 1024 * 1024
POINTER = re.compile(rb"version https://git-lfs.github.com/spec/v1\noid sha256:[0-9a-f]{64}\nsize [0-9]+\n?")

def fail():
    raise ValueError("INVALID_INPUT")

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail()
        result[key] = value
    return result

def safe_name(name, directory=False):
    if not isinstance(name, str) or not name or len(name) > 512:
        return False
    if any(ord(c) < 32 or ord(c) == 127 for c in name) or "\\" in name:
        return False
    text = name[:-1] if directory and name.endswith("/") else name
    return bool(text) and not text.startswith("/") and all(p not in ("", ".", "..") and ":" not in p for p in text.split("/"))

def validate(manifest):
    keys = {"schemaVersion", "sourceRevision", "rootPrefix", "requiredFiles", "requiredPrefixes"}
    if not isinstance(manifest, dict) or set(manifest) != keys or type(manifest["schemaVersion"]) is not int or manifest["schemaVersion"] != 1:
        fail()
    if not isinstance(manifest["sourceRevision"], str) or not re.fullmatch("[0-9a-f]{40}", manifest["sourceRevision"]):
        fail()
    prefix = manifest["rootPrefix"]
    if not isinstance(prefix, str) or (prefix and (not prefix.endswith("/") or not safe_name(prefix, True))):
        fail()
    total = 0
    for field in ("requiredFiles", "requiredPrefixes"):
        names = manifest[field]
        if not isinstance(names, list) or len(names) > 100:
            fail()
        for name in names:
            directory = field == "requiredPrefixes"
            if not safe_name(name, directory) or name.endswith("/") != directory:
                fail()
        if len(set(names)) != len(names):
            fail()
        total += len(names)
    if not 1 <= total <= 100:
        fail()
    return manifest

def read_bounded(path, limit):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        fail()
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        fail()
    return data

def inspect(manifest, archive):
    manifest = validate(manifest)
    if not isinstance(archive, bytes) or len(archive) > MAX_ZIP:
        fail()
    findings, files, seen, folded = [], set(), set(), set()
    with zipfile.ZipFile(io.BytesIO(archive)) as source:
        entries = source.infolist()
        if len(entries) > 10000 or sum(x.file_size for x in entries) > 256 * 1024 * 1024:
            fail()
        for member_index, entry in enumerate(entries):
            name = entry.orig_filename
            if not safe_name(name, entry.is_dir()):
                findings.append({"kind": "UNSAFE_MEMBER_NAME", "memberIndex": member_index})
                continue
            identity = name.rstrip("/")
            if identity in seen:
                findings.append({"kind": "DUPLICATE_MEMBER", "member": name})
            elif identity.casefold() in folded:
                findings.append({"kind": "CASE_COLLISION", "member": name})
            seen.add(identity)
            folded.add(identity.casefold())
            if entry.flag_bits & 1 or entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                fail()
            if stat.S_ISLNK(entry.external_attr >> 16):
                findings.append({"kind": "SYMLINK_METADATA", "member": name})
                continue
            if entry.is_dir():
                continue
            files.add(name)
            if entry.file_size <= 1024:
                with source.open(entry) as stream:
                    sample = stream.read(1025)
                if len(sample) > 1024:
                    fail()
                if POINTER.fullmatch(sample.replace(b"\r\n", b"\n")):
                    findings.append({"kind": "CANONICAL_LFS_POINTER", "member": name})
        root = manifest["rootPrefix"]
        for name in manifest["requiredFiles"]:
            if root + name not in files:
                findings.append({"kind": "MISSING_FILE", "member": name})
        for name in manifest["requiredPrefixes"]:
            if not any(p.startswith(root + name) for p in files):
                findings.append({"kind": "EMPTY_REQUIRED_PREFIX", "member": name})
    return {
        "schemaVersion": 1,
        "evidence": "ZIP_METADATA_AND_SMALL_ENTRY_INSPECTION",
        "declaredRevision": manifest["sourceRevision"],
        "archiveSha256": hashlib.sha256(archive).hexdigest(),
        "configuredChecksSatisfied": not findings,
        "memberCount": len(entries),
        "findings": findings,
        "limitations": [
            "Expected paths and revision are operator assertions; no signature or commit binding",
            "No extraction, network, LFS hydration, full CRC scan, build or secret scan",
            "Nonempty required prefix does not prove a complete submodule checkout",
            "Only strict three-line small LFS pointers are recognized; intentional pointer fixtures also produce findings"
        ]
    }

def main(args):
    if args == ["--help"]:
        return 0, {"usage": "python -B check.py EXPECTATIONS.json SOURCE.zip"}
    try:
        if len(args) != 2 or any(arg.startswith("-") for arg in args):
            fail()
        manifest = json.loads(read_bounded(args[0], MAX_MANIFEST).decode("utf-8"), object_pairs_hook=unique_object)
        result = inspect(manifest, read_bounded(args[1], MAX_ZIP))
        return (0 if result["configuredChecksSatisfied"] else 1), result
    except Exception:
        return 2, {"error": "INVALID_INPUT"}

if __name__ == "__main__":
    code, report = main(sys.argv[1:])
    print(json.dumps(report, ensure_ascii=True), file=sys.stderr if code == 2 else sys.stdout)
    raise SystemExit(code)
