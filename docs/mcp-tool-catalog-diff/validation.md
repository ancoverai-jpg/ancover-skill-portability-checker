# Validation — experimental MCP Tool Catalog Diff

Observed2026-11-05 on Windows/PowerShell7.6, Node24.22.1, Python3.12.14 and Codex CLI0.166.0-alpha.6.

|Check|Observed result|Evidence limit|
|---|---|---|
|Frozen dependency installation|Fresh checkout pnpm install --frozen-lockfile --ignore-scripts passed; Node YAML version/lockfile unchanged|No new dependency; older helpers retain existing Python requirements|
|Behavior|24 Node and44 Python tests passed locally;16 new catalog regressions|Synthetic selected catalogs, not live MCP transport|
|New helper without dependencies|Bundled base Python executed synthetic comparison with expected REVIEW_REQUIRED/1|Standard-library helper; no server process/API calls|
|Invalid input/privacy|Duplicate keys/names, numeric precision/spelling, arrays, partial/wrong-scope/profile, shape/count/depth/node/size limits, actual CLI exit2 and value suppression exercised|Not exhaustive JSON/MCP conformance; hashes can identify known input|
|Read preservation|Actual CLI left both selected snapshot byte strings unchanged|Stable synthetic local files, not concurrent filesystem attack testing|
|Codex lifecycle|Isolated CODEX_HOME: install/list0.5.0, execute installed helper changed/unchanged exit1/0, remove, temporary-copy0.5.1 reinstall/list, partial capture exit2, remove plugin/marketplace; final list empty|Manual reinstall, not automatic app update; personal config SHA256 unchanged|
|Codex conversation|NOT_TESTED|No trigger or agent improvement claim|
|Claude Code|NOT_TESTED; executable unavailable|No stable cross-host certification|
|Standalone Skill-only distribution|NOT_TESTED; full package/docs layout used|Do not infer standalone installation support|
|Static preflight|No findings; six canonical Skills|Static subset, not safety/runtime certification|
|Node dependency advisory lookup|pnpm audit --prod reported no known vulnerabilities|Point-in-time database result, not dependency safety assurance|
|CI|Existing workflow installs older-helper pinned requirements and runs all tests on Windows/Ubuntu|Exact head/merge run must be verified before release; this text alone does not establish success|

MIT package, no new dependency or copied third-party source. Exact-file/privacy/license review and remote inventory/commit are recorded separately in publication evidence. UNCHANGED is selected-data equality under this profile, not authenticated execution, semantic compatibility, permission approval or behavior stability.
