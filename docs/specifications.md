# First three candidate specifications

## 1. Skill Preflight — experimental pilot, 0.1.0

Problem: metadata and package differences can prevent Skills from loading. Three independent project reports and current upstream alternatives are recorded in research.md and pilot-evidence.json. Some reports are fixed; do not market their old defects as current.

Primary user: maintainer preparing a local Skill/plugin for distribution. Flow: install checker dependencies with scripts disabled → select local target → run offline checker → review JSON and tree digest → correct findings → separately exercise each host. Inputs: directory. Outputs: JSON/stdout, exit status. Permissions: read target, no network during inspection. Installation needs network for dependencies.

Scope: required metadata types and lengths, conservative ASCII name profile, package overlay consistency, inline local Markdown files, symlinks, filenames and content digest. Excludes full schemas, executing target code, remote URLs/anchors, secret-content scanning, security approval and provenance signatures. Alternative: official skills-ref and host validators; differentiation is one small cross-package review artifact, not a replacement standard.

Architecture: canonical skills/, portable manifest, Codex/Claude overlays, Node CLI using pinned YAML parser. No new server. Acceptance: stable digest on unchanged fixture; changed content changes digest; invalid metadata/link/private-name fixtures fail; invalid invocation has nonzero exit; output never includes fixture secret contents; lock conflict cannot commit concurrent state. Official-host invocation coverage is separate.

Evaluation defined before comparison: synthetic fixture contains metadata name mismatch, missing local file and private filename. Baseline checks only SKILL.md existence; treatment uses checker. Score correct findings and avoid false runtime/safety claims. This measures deterministic fixture coverage only, not model quality, productivity or real-world security. Agent with/without-Skill evaluation remains pending; no claim of improvement by the instruction Skill.

Demo: run valid self-package and malformed synthetic package. Maintenance: watch upstream specs monthly and on reported failures; add regressions for observed bugs. Release experimental until separate host installation and trigger coverage is sufficient.

## 2. Release evidence handoff — specification only, demand hypothesis

Problem: maintainers need to distinguish documented examples from commands actually exercised. Current documentation leads are one-community samples and do not qualify demand. Primary user: release reviewer. Flow: select project and release → map advertised examples to observed test artifacts → report missing coverage → prepare reviewer handoff.

Inputs: local README, tests, CI artifacts and consented logs. Outputs: Markdown evidence matrix plus JSON. Read-only by default; execute only approved project commands in isolation and redact logs. Scope: provenance of release claims. Excludes running unknown install scripts automatically, performance claims from mocks and replacing existing test frameworks. Alternatives: CI artifacts, MkDocs/link checkers and manual checklists. Proposed gap: explicit claim-to-execution mapping with revision identity.

Architecture: instruction Skill plus small artifact normalizer only if repeated work justifies it. Acceptance: every advertised claim has a source revision, method and status; unavailable runs are NOT_TESTED; redaction fixtures do not reveal secret values. Evaluation: preregister claims in a seeded release, compare manual baseline and Skill-assisted review for missed/incorrect mappings. Demo: a synthetic README advertises one working and one unavailable example. Maintenance: generic schemas first, no fragile CI-provider integrations until demand qualified. Build gate: obtain three independent reports in two communities and review existing solutions first.

## 3. Environment contract diagnosis — specification only, demand hypothesis

Problem: environment precedence and redaction affect configuration troubleshooting; Docker Compose reports are leads, not sufficient independent demand. Primary user: platform engineer. Flow: inspect sanitized config declarations → map required keys and precedence → flag missing/contradictory contracts → produce suggested corrections.

Inputs: consented config schema and templates without secret values. Outputs: names-only contract graph and actionable report. Permissions: local read; no production mutation or environment dump. Scope: declared keys and documented precedence. Excludes deployment, printing resolved secrets and claiming runtime connectivity. Alternatives: docker compose config, schema validators and existing secret scanners. Proposed gap: names-only handoff safe to attach to issues; validate differentiation through user feedback.

Architecture: Skill plus format-specific parser adapters if justified. Acceptance: no values in output/errors; synthetic missing and conflicting keys detected; unsupported interpolation explicitly unknown; original config unchanged. Evaluation: compare task outcomes against existing Compose diagnostics using predefined fixtures and false-positive review. Demo: synthetic service missing a required variable. Maintenance: lock supported Compose versions; triage semantics changes before adding formats. Build gate: qualify evidence in two independent communities; never implement destructive remediation by default.
