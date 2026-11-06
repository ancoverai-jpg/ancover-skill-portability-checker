---
name: git-tracked-ignore-review
description: Inspect the current Git index for paths matching repository .gitignore rules. Use when a file still appears in Git after adding an ignore rule or when reviewing the scope of a publication.
license: MIT
---
# Git tracked ignore review

Select the full worktree root and establish which ignore rules the operator intended to apply. Git applies ignore rules when considering untracked paths. An indexed path can still match those rules. This is common when a generated file was indexed before the rule was added.

Run the helper from the trusted package root or resolve it from this installed Skill. Use Python 3.12 and a trusted Git on PATH.

```sh
python -I -B skills/git-tracked-ignore-review/scripts/check.py WORKTREE_ROOT
```

The output gives the unique match count and a digest of the path set. Exit 0 reports NO_INDEX_MATCHES under the repository-rule scope. Exit 1 reports INDEX_MATCHES for review. Exit 2 reports INDETERMINATE. A match can be intentional. Read the [profile](references/profile.md) before interpreting the result.

When the operator needs the names, inspect them locally with Git.

```sh
git -C WORKTREE_ROOT ls-files --cached --ignored --exclude-per-directory=.gitignore
```

For a single approved path, Git check-ignore with --no-index and -v can identify the matching rule. Check the source and whether the displayed pattern is a negation. The query also considers local exclusions. Keep names, rule text and output from verbose Git commands in the private review.

Report the match count, digest, rule scope and whether the result calls for human review. The index and available .gitignore files describe the selected worktree at inspection time. Review actual staged changes and historical exposure separately when those questions are in scope. Any index or history edit requires its own explicit scope.
