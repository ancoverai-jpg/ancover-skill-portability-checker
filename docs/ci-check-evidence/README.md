# CI Check Evidence (experimental candidate)
Offline review of an explicit expected-check policy against one supplied GitHub check-run snapshot. This is a proposed additional Skill in Ancover Skill Portability Checker, not another service or a merge gate.
Use Node22+; no dependency installation is needed for this helper:
```sh
node skills/ci-check-evidence/scripts/check.mjs examples/ci-check-evidence/missing-context.json
```
The synthetic example intentionally exits1 and reports missing integration evidence.
See [contract](../../skills/ci-check-evidence/references/contract.md), [Skill](../../skills/ci-check-evidence/SKILL.md) and [validation](validation.md). Installation: copy skills/ci-check-evidence to the host's project .agents/skills (Codex) or .claude/skills (Claude Code), or use the existing package's plugin install. Remove only the installed Skill directory to uninstall; update by reviewing the diff, replacing that directory and rerunning the example.
No values or logs are emitted. Approved check names and app IDs remain visible; review those before sharing. Input authenticity and expected policy are supplied by the operator. Zero exit means only that supplied policy is satisfied, including any explicitly allowed skips. It does not mean all tests ran, branch rules permit merging, or deployment is safe.
No network, tokens, reruns, rule edits or command execution. JSON input is bounded and errors are fixed. Do not treat file handling as a hostile-filesystem sandbox.
License: existing repository MIT. Report sensitive bugs through the repository's private vulnerability reporting; never attach tokens or private job logs. Changes should preserve the explicit skip distinction and fixed error behavior. Tests: node --test tests/ci-check-evidence.test.mjs.
Roadmap: review actual workflows and check naming variations; keep unsupported GitHub semantics explicit before adding formats. No automated remediation planned. Changelog: experimental0.1.0 adds expected-context, revision, completeness and skip-policy review.
Host conversational behavior and Claude runtime are NOT_TESTED; installation lifecycle, script execution, fixtures and remote CI are separate evidence.
