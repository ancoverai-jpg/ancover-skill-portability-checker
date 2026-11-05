# Ancover Skill Portability Checker

Experimental tools for maintainers distributing agent Skills across Codex and Claude Code.

[![Validation](https://github.com/ancoverai-jpg/ancover-skill-portability-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/ancoverai-jpg/ancover-skill-portability-checker/actions/workflows/ci.yml)

The first pilot, **Skill Preflight**, reads a local package and reports a deliberately small set of portability and hygiene findings. Its tree digest lets reviewers identify the content inspected. It does not certify safety, execute target code or establish host compatibility.

[Português do Brasil](README.pt-BR.md) · [Research and ranking](docs/research.md) · [Specifications](docs/specifications.md) · [Operations](docs/operations.md) · [Validation](docs/validation.md)

## Quick start

Requires Node.js 22+ and pnpm 11.25.0. Download or clone this source, open its root, and run:

```sh
git clone https://github.com/ancoverai-jpg/ancover-skill-portability-checker.git
cd ancover-skill-portability-checker
pnpm install --frozen-lockfile --ignore-scripts
node --test tests/*.test.mjs
node skills/skill-preflight/scripts/check.mjs .
```

Use an absolute directory instead of `.` to inspect another package. Exit codes: 0 passed these rules, 1 findings, 2 invalid invocation or inspection failure. Reports contain paths, rule IDs and hashes, never source contents. Dependencies are fetched only at installation; the checker itself is offline.

Example output fields (run the command for actual values):

```json
{"evidence":"STATIC_INSPECTION","profile":"ancover-portable-v0.1","passed":true,"runtime":{"codex":"NOT_TESTED","claudeCode":"NOT_TESTED"}}
```

## Agent use

One canonical `skills/` directory backs the portable root manifest and the Codex and Claude overlays. Invoke the bundled Skill and point it at the local target. Host checks and trigger tests are documented separately in the validation report. The `portfolio-research` Skill guides daily research and maintenance toward the user-requested target of three new projects or Skills actually published per day, using only the 12:00, 18:00 and 21:00 São Paulo windows; after three, maintain/prepare without new publication, with unchanged evidence and quality gates.

For a temporary Claude Code development session, the documented upstream path is `claude --plugin-dir /absolute/path/to/ancover-open-source`. This host is unavailable here; validate with `claude plugin validate` and test real invocation before claiming compatibility. Codex installation procedures and their observed results are recorded in the operations guide.

## Architecture and limits

`skills/skill-preflight/scripts/check.mjs` provides deterministic, read-only inspection. `scripts/program.mjs` maintains an operator ledger with exclusive locks, atomic snapshots and publication gates. The scheduled agent performs research and development; the deterministic runner does not generate code or publish by itself.

Checked: required metadata, ASCII kebab-case profile, manifest identity/version drift, inline Markdown local files, symlinks, private-looking filenames, file count/size bounds and content digests. Unchecked: full host schemas, remote links, heading anchors, embedded secrets, script behavior, prompt injection, signatures and publisher identity. Dependency/Git/runtime directories are excluded from the digest. Inspect a stable, trusted filesystem snapshot; this is not a sandbox against concurrently changing files.

No telemetry or remote upload. Do not submit sensitive package paths in public reports. YAML is the Node checker dependency; the optional MCP helper has six pinned Python dependencies installed separately; see the lockfile and [security policy](SECURITY.md). Read [contribution guidance](CONTRIBUTING.md), [roadmap](ROADMAP.md) and [changelog](CHANGELOG.md). MIT licensed. No copied REA code or assets.

## CI Check Evidence — experimental

The [ci-check-evidence Skill](skills/ci-check-evidence/SKILL.md) reviews an explicit expected-check policy against an operator-supplied, single-revision snapshot. It flags missing contexts, unapproved skips, revision mismatches and ambiguous app/context identities. It does not run tests, read rulesets or approve merges. See [documentation and coverage](docs/ci-check-evidence/README.md).

## Source Archive Review — experimental

[Source Archive Review](skills/source-archive-review/SKILL.md) inspects a selected ZIP against explicit expected files/prefixes and flags strict small Git LFS pointers, without extraction. Requires Python3.10+; no pip packages. See [EN documentation](docs/source-archive-review/README.md) and [Português](docs/source-archive-review/README.pt-BR.md). It does not establish a successful build, full payload integrity or provenance.

Run the Python profile tests separately with: python -B -m unittest discover -s tests -p "*_test.py".

## MCP Structured Result Check — experimental

[MCP Structured Result Check](skills/mcp-structured-result-check/SKILL.md) compares one recorded legacy MCP structuredContent object with its selected outputSchema. It distinguishes mismatches, tool-reported errors and unsupported validation, suppressing payload data in its report. Requires Python3.12+ and the isolated pinned requirements. [EN documentation](docs/mcp-structured-result-check/README.md) · [Português](docs/mcp-structured-result-check/README.pt-BR.md). No live transport, successful real tool execution or modern protocol compatibility is inferred.
