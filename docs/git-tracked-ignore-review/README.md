# Git Tracked Ignore Review

This experimental Ancover Skill checks which paths in a Git index match repository .gitignore rules. It helps review publication scope after changing an ignore rule. The helper uses Git and Python 3.12 standard library. [Skill](../../skills/git-tracked-ignore-review/SKILL.md) · [Research](research.md) · [Specification](specification.md) · [Português](README.pt-BR.md)

From a trusted package directory, pass the root of a regular Git checkout.

```sh
python -I -B skills/git-tracked-ignore-review/scripts/check.py WORKTREE_ROOT
```

A reproducible positive example uses a disposable repository. Replace EXAMPLE with a new empty directory reserved for the demonstration.

```sh
git init EXAMPLE
cd EXAMPLE
```

Create a file named sample.log with synthetic text. Run git add -- sample.log, then create .gitignore with one line containing *.log. Invoke the helper by its absolute trusted path against the current worktree root (a dot from the scratch repository). The expected result is INDEX_MATCHES with count 1 and exit 1. A fresh empty Git worktree should return NO_INDEX_MATCHES with count 0 and exit 0. A path outside a Git worktree should return INDETERMINATE and exit 2. The test suite builds and runs these repositories with Git.

Rules come from the available per-directory .gitignore files. Standard local and machine exclusions have a separate scope. Matching is evaluated against the index, including uncommitted staged paths. The report identifies the matched path set without raw names or file contents. The digest can identify known inputs. Use the private Git command in the Skill to locate entries before drawing a conclusion.

The helper runs fixed Git queries with optional writes and prompts disabled. Use a stable trusted checkout and Git installation. Each query times out after ten seconds. The accepted output limit is 1 MiB per command, checked after capture. Coverage focuses on the selected index, so history and other worktrees need separate evidence. Sparse checkouts and standalone Skill-only installation are NOT_TESTED.

Install the complete package through an isolated plugin marketplace or invoke the helper from its trusted source checkout. To update, review the new package and repeat the example. Remove only the selected plugin installation. [Validation](validation.md) describes the tested lifecycle and host limits. The package uses MIT licensing. Git is a separate system prerequisite.

## Run the reproducible fixtures

~~~sh
python -I -B -m unittest discover -s tests -p git_tracked_ignore_test.py
~~~
