# Validation

Experimental package observed locally on 2026-11-06 with Windows, Git 2.56.0.windows.4, Python 3.12, Node 24.22.1 and Codex CLI 0.166.0-alpha.6.

| Check | Observed result |
|---|---|
| Package | Frozen pnpm install with lifecycle scripts disabled. Static preflight found seven canonical Skills and zero findings. |
| Tests | 24 Node and 52 Python tests passed locally, including eight new Git regressions. |
| Real Git workflow | A disposable checkout produced zero matches before adding a rule and one indexed match afterward. The current source checkout also returned zero matches. |
| Invalid inputs | Missing Git, missing path, wrong argument count, subdirectory, non-repository, bare repo and index override returned INDETERMINATE. |
| Rule behavior | Nested rules and negation exercised real Git. The standard-exclusion control found local and global matches that are outside the repository profile. |
| Privacy and preservation | The synthetic path, private value and absolute root were absent from stdout. Index and selected file bytes stayed identical. |
| Codex lifecycle | Isolated install and list at 0.6.0, installed helper exit 0 and 1, removal, reinstall from a temporary 0.6.1 copy, installed helper exit 2 and removal. The final installed list was empty and the personal config digest stayed identical. |
| Codex conversation | NOT_TESTED. |
| Claude Code | NOT_TESTED. The executable was unavailable on PATH. |
| Sparse checkouts and standalone Skill installation | NOT_TESTED. The full plugin package and ordinary worktrees were used. |
| CI | Windows and Ubuntu run the existing Node and Python workflow. Exact commit and job outcomes are recorded as publication evidence. |

The helper uses Python standard library and an existing trusted Git installation. The MIT package license and existing third-party notices apply. Git is a separate prerequisite. Report coverage concerns paths in the selected index and per-directory rules.
