# Validation — experimental 0.1.0

Environment: Windows, PowerShell 7.6, Node v24.19.0, pnpm 11.25.0, Codex CLI 0.163.0-alpha.10.2. Date: 2026-10-17 local. Retrieval/evidence timestamps may be 2026-10-18 UTC.

| Check | Method and result | Evidence type |
|---|---|---|
|Frozen install|Separate clean source copy, no node_modules, pnpm install --frozen-lockfile --ignore-scripts succeeded|Real local dependency installation; store cache reused|
|Behavior tests|11 tests passed, zero failed/skipped, including five distinct Skills sharing one repository and local-day counting|Real local execution on synthetic fixtures|
|Valid package|Checker accepted source with no findings|Static inspection executed locally|
|Invalid inputs|Seeded name mismatch, missing file and private filename detected; exit 1|Real script execution on synthetic fixture|
|Missing target/dependency|Both returned environment error exit 2|Real negative execution|
|Output redaction|Synthetic sentinel absent from stdout|Real fixture observation; not general secret detection|
|Digest binding|Unchanged fixture stable; changed content changed digest|Real deterministic test|
|Symlink/escaping link|Rejected without target traversal|Real synthetic filesystem tests|
|State/locks|Transaction rollback, overlap exclusion, cycle lease ownership and duplicate ideas exercised|Real local process/filesystem tests|
|Demand/quality/publication gates|Insufficient demand, blockers, missing remote evidence and duplicates rejected; obsolete weekly cap removed|Deterministic unit tests, not actual GitHub publication|
|Skill authoring validator|Both Skills passed bundled quick_validate.py after isolated PyYAML installation|Static metadata validation|
|Dependency advisory lookup|pnpm audit --prod reported no known vulnerabilities|Point-in-time registry advisory check; not assurance of safety|
|Codex installation|Isolated CODEX_HOME; marketplace added; 0.1.0 installed, listed enabled, removed|Real host CLI lifecycle|
|Codex update path|Modified isolated package to 0.1.1, reinstalled, confirmed two Skill directories, removed; installed list empty|Real host CLI reinstall lifecycle; not app auto-update|
|Codex conversation|Explicit and automatic positive/negative trigger evaluation pending|NOT_TESTED|
|Claude Code|Executable absent; documented procedure supplied|NOT_TESTED|
|CI|Windows and Ubuntu jobs passed with Node 22, frozen dependency installation, 11 tests and self-inspection on commit d6d2534d3319844ed79830407ce0fbede77c6c17|Real GitHub Actions execution; run 39087680324|
|Ancover App plugin|Updated to 1.0.2; read-back confirmed daily research target, preserving identity, App connection and presentation|Real saved release plus source verification; new-session host behavior NOT_TESTED|
|Ancover discovery tools|list_plugins and search_public_capabilities returned -32603 Internal error|Observed failed calls; no runtime trust claim|
|Public GitHub|Public repository created; 33 source files in commit d6d2534d3319844ed79830407ce0fbede77c6c17 matched local bytes through an unauthenticated Git clone|Actual source publication, verified separately from experimental host coverage|
|Daily recurrence|Existing heartbeat updated ACTIVE to 09:00, 12:00, 15:00, 18:00 and 21:00; local schedule record inspected|Actual scheduler configuration, future execution NOT_TESTED|

Commands: `pnpm install --frozen-lockfile --ignore-scripts`; `node --test tests/*.test.mjs`; `node skills/skill-preflight/scripts/check.mjs .`; `pnpm audit --prod`; `node scripts/discover.mjs .runtime/discovery-latest.json`; `node scripts/program.mjs cycle`. Discovery collector completed all eight queries in the final smoke run; these results are unreviewed leads and do not automatically qualify candidates.

The standalone checker was used in this chat against valid and invalid local fixtures. That establishes useful script execution, not automatic Skill selection in a fresh host session. The existing Ancover research Skill was read back after saving, but requires a fresh-session behavioral check. No agent-with/without-Skill improvement claim is made.

## Baseline comparison

Before running the comparison, the pilot specification defined three seeded defects and a baseline that checks SKILL.md existence only. Baseline detected 0/3; the checker detected 3/3 and did not print the synthetic sentinel. This narrow deterministic result is in the separate delivery evidence `demo-comparison.json`. It is not an agent A/B benchmark or an estimate of productivity, broad security detection or field performance.

## Remaining gates

The pilot is suitable for an **experimental source publication**, with the supported local CLI checks passing. Conversational invocation/trigger evaluation in Codex and Claude Code runtime checks remain NOT_TESTED; they block a stable cross-host claim, not disclosure of this explicitly experimental source. Inspect the GitHub Actions run for actual CI results. Repository creation/write access was verified after the initial reports. The exact candidate source inventory was reviewed and common GitHub/OpenAI token and private-key patterns produced zero matches; this bounded scan is not proof that all possible secrets are absent. Filename checks and advisory queries alone are insufficient. No badges, screenshots or testimonials were fabricated.
