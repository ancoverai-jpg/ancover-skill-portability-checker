---
name: source-archive-review
description: Review a small source ZIP against explicit expected files and submodule-content prefixes, and flag canonical Git LFS pointers without extracting the archive. Use before distributing source archives, not to certify builds or hydrate dependencies.
license: MIT
---
# Source archive review
Use for a maintainer checking the actual source ZIP offered to users without a Git checkout. Distinguish auto-generated GitHub source archives from independently packaged release assets.

Pin the intended revision and identify build prerequisites from that revision's source/build configuration. Gitlinks can establish submodule paths; do not infer a complete submodule from .gitmodules or one nonempty directory. Record authoritative representative required files when possible. Manifest paths and sourceRevision remain operator assertions, not cryptographic provenance.

Read [the profile and contract](references/profile.md). Supply an explicit rootPrefix matching the selected artifact; do not guess or silently strip archive roots. Run:
```sh
python -B skills/source-archive-review/scripts/check.py EXPECTATIONS.json SOURCE.zip
```
The helper reads metadata and small members only. It never extracts, downloads, hydrates LFS, changes archive settings, executes source or installs dependencies. Findings require review; an intentional pointer test fixture also matches the canonical-pointer rule.

Treat missing prerequisites, empty expected prefixes, ambiguous names, link metadata or pointer findings as unresolved distribution questions. A zero exit satisfies only the supplied profile. It does not establish source completeness, integrity of every payload, successful compilation, signature authenticity, absence of secrets or safe extraction.

If the artifact needs correction, prefer the project's established distribution/packaging tools, such as git-archive-all, and independently inspect the resulting artifact. Do not change LFS settings or perform paid/bandwidth-consuming object downloads without the applicable authorization. Do not rerun Git commands inside a downloaded source ZIP as though it were a checkout.

Report artifact SHA256, declared revision and expectation origin, profile limits, findings, and the next actual build/source check. Keep local paths, source contents and LFS OIDs out of shareable diagnostics; approved member names remain visible. Separate this static review from any isolated build, including commands and outcomes when a build is separately authorized.
