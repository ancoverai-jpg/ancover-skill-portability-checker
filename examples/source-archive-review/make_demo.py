"""Create a synthetic review fixture in a NEW directory; never overwrite inputs."""
import json
import sys
import zipfile
from pathlib import Path
if len(sys.argv) != 2:
    raise SystemExit("Usage: python make_demo.py NEW_DEMO_DIRECTORY")
root = Path(sys.argv[1])
root.mkdir(parents=False, exist_ok=False)
manifest = {"schemaVersion": 1, "sourceRevision": "a" * 40, "rootPrefix": "repo/", "requiredFiles": ["README.md", "main.py"], "requiredPrefixes": ["vendor/library/"]}
(root / "expectations.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
with zipfile.ZipFile(root / "source.zip", "w", zipfile.ZIP_DEFLATED) as source:
    source.writestr("repo/README.md", "Synthetic source; intentionally incomplete.")
print("Created synthetic fixture; expected review exit code 1.")
