# Demand and prioritization

Sources were retrieved on 2026-11-06. The audience is maintainers reviewing publication scope after adding or changing repository ignore rules. The recurring problem is the difference between a path matching a rule and a path remaining in the index.

| Independent report | Observed problem |
|---|---|
| [VS Code issue #160653](https://github.com/microsoft/vscode/issues/160653), memeplex, 2022-09-11, open at retrieval | The author reports confusing editor feedback for an indexed path that also matches an ignore rule. The report concerns VS Code 1.71.0. |
| [GSD issue #703](https://github.com/gsd-build/get-shit-done/issues/703), begna112, 2026-02-22, closed at retrieval | The author reports that a default check-ignore call overlooked the rule match for indexed planning files and changed the outcome of an automated commit decision. |
| [Stack Overflow question #28101020](https://stackoverflow.com/questions/28101020/git-status-is-showing-changes-not-staged-for-commit-for-files-listed-in-gitig), WestCoastProjects, 2015-01-23 | The author observes modified XML files remaining visible after adding their paths to .gitignore. |

These three firsthand reports come from three authors and three communities, including two separate platforms. Issue states and historical observations describe the source evidence. Current application defects were not reproduced.

Git already provides the correct query with ls-files in cached and ignored mode. Its documentation distinguishes per-directory exclude files from standard exclusions. check-ignore with --no-index helps inspect a specific rule match. The Skill adds a repeatable release-review procedure and a bounded report that suppresses filenames. Git remains the rule engine. [Git ls-files manual](https://git-scm.com/docs/git-ls-files) · [Git check-ignore manual](https://git-scm.com/docs/git-check-ignore) · [Git ignore rules](https://git-scm.com/docs/gitignore)

Editorial scores on a 1–5 scale are pain 3, evidence 4, gap 2, demonstrable value 3, adoption 1, Skill fit 4, enterprise relevance 3, maintenance 4 and Ancover fit 4. Git supplies the essential capability, which makes the incremental gap narrow and maintenance modest. The workflow fits a handoff between repository owners and release reviewers. Adoption and time savings are unmeasured. Confidence is high in the Git behavior and moderate in the incremental usefulness of the report. One focused pilot is feasible with Git and Python standard library.
