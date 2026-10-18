# Operation and maintenance

## Manual cycle

From this package root, install dependencies using `pnpm install --frozen-lockfile --ignore-scripts`, then run:

```sh
node scripts/program.mjs status
node scripts/program.mjs cycle
```

The same state and handoff are used by the scheduled agent. `cycle` prioritizes maintenance/published/validating/developing items over new ideas. It does not perform research, execute arbitrary scripts or publish on its own. The portfolio-research Skill supplies the agent procedure. State defaults to `.runtime/state.json`; override with `ANCOVER_STATE_DIR`. Private runtime files are never distributed.

Collect bounded public leads with `node scripts/discover.mjs .runtime/discovery-latest.json`. This makes eight public GitHub searches with 15-second request timeouts and at most four results per niche. It records dates and authors without collecting credentials or source code. Errors are categorized without response bodies. Review relevance, independence and current alternatives manually before advancing a candidate. A successful fetch is not a qualified opportunity.

Add an idea with `node scripts/program.mjs add skill-preflight "Skill portability preflight"`. `advance ID STAGE JSON` requires an artifact reference. Stages are discovered → researched → prioritized → specified → developing → validating → ready → published → maintenance. Demand needs three independent reports in two communities. Ready needs zero blockers, passed validation and a digest. Published needs the verified remote URL and commit. The user replaced the weekly cap with a target of **at least five new projects or Skills per local day** in America/Sao_Paulo. Count distinct units only; a Skill needs `unit: "skill"` and its `skills/name/SKILL.md` path. Related Skills can share a repository; duplicate paths/units are rejected. Private plugin saves, drafts and version-only updates do not count. `cycle` reports the actual daily total and deficit. These are recorded assertions supplied by an authorized operator; the state machine does not independently verify GitHub or prevent the owner editing JSON. Automated publication is not implemented in the deterministic runner.

Before agent work, acquire the whole-cycle lease with `node scripts/cycle-lease.mjs acquire UNIQUE-RUN-ID` and set `ANCOVER_CYCLE_ID` to that ID for ledger mutations. Release with `node scripts/cycle-lease.mjs release UNIQUE-RUN-ID`. The lease prevents a second scheduled agent from starting conflicting work; ledger commands reject another owner's ID. An operator must respect the lease for external actions too. After a crash, inspect its start time and the actual running thread before removing a stale lease; no timed auto-expiry can interrupt a live cycle.

The shorter transaction `cycle.lock` contains PID/start time. A conflicting state write fails. State and history commit together via temporary file and atomic rename. An interrupted transaction preserves the last committed state. Remove a stale transaction lock only after confirming its PID is no longer running. A dependency/network failure gets at most two attempts; record redacted error categories and leave a resumable handoff.

Limits per scheduled window: 45 minutes, two attempts per failing external action and zero paid API calls/service purchases. There is no weekly publication cap. The daily target does not waive evidence or quality requirements. The heartbeat agent must enforce time and action budgets; these are not OS-enforced kill switches. Do not start a long operation near the limit. Save partial work and continue next window. No cost measurement is fabricated; the Codex account's normal usage limits apply.

## Recurrence

The existing Codex thread heartbeat `ancover-open-source-ciclo-semanal` retains its stable ID and was updated in place to daily windows at **09:00, 12:00, 15:00, 18:00 and 21:00 America/Sao_Paulo**, with status ACTIVE. The displayed name reflects the five-publications daily target. The previous Monday schedule is superseded. An immediate manual cycle began on 2026-10-17. Scheduled execution depends on desktop host availability, sign-in, network, connected-tool permissions and scheduler behavior; future runs and five actual publications are not guaranteed by the schedule. Stay quiet for unchanged/non-actionable conditions; notify publications, material failures and required decisions. Do not repeatedly notify known blockers unless they change.

## Installation, update and uninstall

For local CLI use, a clean copy with dependencies installed is sufficient. The checker makes no target writes. Update by reviewing the source diff and lockfile, installing frozen dependencies and rerunning tests. Uninstall by removing only the selected package directory; no global settings are changed by the checker.

Codex development: the official local marketplace uses `.agents/plugins/marketplace.json`, an entry with `source: {source: "local", path: "./plugins/ancover-skill-portability-checker"}`, and an isolated copy under `plugins/`. Use a temporary CODEX_HOME to validate lifecycle without changing the user's existing settings. Register with `codex plugin marketplace add ABSOLUTE_MARKETPLACE_ROOT`, install using `codex plugin add ancover-skill-portability-checker@ancover-local`, list, remove and re-add to exercise update. Record actual results in validation.md. No completed host run is inferred from the CLI merely being present.

Claude Code development: `claude plugin validate ABSOLUTE_PLUGIN_ROOT`, then `claude --plugin-dir ABSOLUTE_PLUGIN_ROOT`. In a fresh session invoke `/ancover-skill-portability-checker:skill-preflight` against a synthetic fixture. Test positive trigger (prepare a Skill for sharing) and negative trigger (audit an API); inspect actual tool use and output. Then test changed source/reload and removal. Claude Code is currently unavailable here, so these steps remain NOT_TESTED.

For both hosts, compare the original host configuration before/after the isolated lifecycle, confirm no unrelated changes, and test a missing Node/dependency path. The compatibility overlays share the same source content and are not separate product implementations.

## Publication and maintenance

Confirmed destination: `ancoverai-jpg`. Public repository: `ancover-skill-portability-checker`, description "Evidence-led Skills and portability tools for agent workflows", MIT, experimental 0.1.0. First close blocking local failures, review the exact manifest/archive and dependency license/security results, and establish working GitHub repository creation permissions. Push without force, inspect the remote tree and commit, and check CI. For existing projects use PRs. Never change private repositories to public. Enabling GitHub private vulnerability reporting remains a post-creation step.

No public marketplace submission is included. A repository release is distinct from directory review. Triage useful issues and outside contributions daily before new production; installations are unavailable unless a distribution channel supplies measured data. No telemetry is present. Do not treat stars as adoption proof. Stop new product work while blocking defects exist.

## Publication identity

The standalone pilot package is named `ancover-skill-portability-checker`, matching its public repository. Earlier isolated installation observations used the working name ancover-open-source; they are historical evidence. The private Ancover IA App plugin keeps its existing identity. GitHub repository creation and push/admin permissions were verified in the authenticated account. The repository contains experimental source; stable cross-host certification is not claimed.
