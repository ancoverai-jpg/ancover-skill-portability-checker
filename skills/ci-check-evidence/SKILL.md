---
name: ci-check-evidence
description: Review expected GitHub CI checks against a supplied revision snapshot, keeping missing contexts and unexpected skips visible. Use for CI evidence review, not for running tests or authorizing merges.
license: MIT
---
# CI check evidence
Use when a maintainer asks whether CI evidence covers the expected checks for a specific revision. Do not route ordinary test execution or automatic merge requests here.

First pin the target commit and identify the expected check names and GitHub App IDs from the maintainer's approved configuration. If the ruleset cannot be read, state that the expected list is operator-supplied; do not invent the repository's required checks. Distinguish the PR head, test merge commit and merge-group revision. Never combine observations from different revisions.

Collect every relevant check-run page for the selected revision using available GitHub tools. Observe the current attempt explicitly. If pagination or freshness is uncertain, retain complete:false. Names alone do not identify an app; similarly named or repeated contexts require review, not a guessed winner. Never disclose logs, credentials or private source when preparing a shareable snapshot.

Read [the input contract](references/contract.md) and normalize only the approved fields. Run the offline evaluator:
```sh
node skills/ci-check-evidence/scripts/check.mjs SNAPSHOT.json
```
The script does not fetch, run, rerun or approve checks. Its supplied revision and completeness fields are assertions, not independently authenticated evidence.

Interpret RECORDED_SUCCESS as the supplied context's reported conclusion. POLICY_ALLOWED_SKIP satisfies only the explicit review policy and counts separately; it does not demonstrate execution. MISSING, AMBIGUOUS, PENDING, UNEXPECTED_SKIP, NON_SUCCESS, REVISION_MISMATCH and INCOMPLETE_SNAPSHOT require concrete follow-up. Exit2 means invalid input, not a clean result.

Report the target revision, source/selection method, expected-list origin, policy result, allowed skips, ignored contexts, gaps and one next check. Avoid the phrase "all tests pass" when only context conclusions were read. Suggest a minimal workflow correction using official documentation when justified; do not change rulesets, disable protection, merge, rerun or publish anything unless separately authorized.
