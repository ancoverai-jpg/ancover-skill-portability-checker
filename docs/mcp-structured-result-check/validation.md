# Validation — experimental MCP Structured Result Check

Observed on local day2026-11-04 (UTC2026-11-05). Windows PowerShell7.6, Python3.12.14, Node24.22.1, pnpm11.25.0, Codex CLI0.166.0-alpha.6.

|Check|Observed evidence|Limit|
|---|---|---|
|Dependency installation|Clean isolated Python venv, six pinned/hash-checked wheels installed; frozen pnpm install with lifecycle scripts disabled|No global dependency changes; Python3.12 is the tested version|
|Behavior|28 Python tests passed (16 new+12 archive),24 Node tests passed; synthetic CLI sample MATCH|Selected synthetic captures; no live server/transport call|
|Negative behavior|Invalid types, required/extra fields, arrays/composition/refs, missing/null payloads, error flags, absent/invalid/unsupported schemas, duplicate/malformed/deep/oversize JSON, numeric overflow and worker timeout exercised|Not exhaustive JSON Schema conformance testing|
|Privacy|Actual CLI mismatch omits synthetic sentinel and secret-field name; no raw library exceptions|Bounded observation, not a general anonymization certificate|
|Missing dependency|Actual base-Python invocation returns INDETERMINATE/DEPENDENCIES_UNAVAILABLE|Does not silently pass|
|Codex lifecycle|Isolated CODEX_HOME: install/list0.4.0, execute installed helper valid sample, remove, modified temporary-copy version0.4.1 reinstall/list, installed invalid fixture exit1, remove plugin/marketplace, final list empty|Manual reinstall, not app automatic update; personal config digest unchanged|
|Codex conversation|NOT_TESTED|No trigger or agent quality claim|
|Claude Code|NOT_TESTED; executable unavailable|No stable cross-host compatibility claim|
|Static preflight|No findings, five canonical Skill paths before final source review|Static subset, not runtime certification|
|Advisories|pnpm audit --prod and OSV querybatch for six exact Python versions returned no known advisories on2026-11-05UTC|Point-in-time database query, not proof of dependency safety|
|CI|Windows/Ubuntu workflow installs pinned wheels and runs all Node/Python tests|Verify the exact reviewed head/merge commit in GitHub Actions before release; this file alone does not establish success|

The report binds only the selected file digest and supplied schema profile. No business-correctness, protocol conformance, authenticated execution, adoption or productivity claim. Package remains experimental. The publication ledger records exact reviewed file inventory, actual remote commit and CI run separately.
