# Repository ignore rule profile

The helper accepts a trusted full Git worktree root. It queries index entries against per-directory .gitignore files using Git itself. Its profile excludes machine-wide rules and .git/info/exclude. The current worktree rules can differ from staged rule files. Git selection overrides, unsupported roots and Git diagnostics yield INDETERMINATE.

Output fields are limited to fixed labels, a count and a SHA256 over sorted unique path bytes with NUL terminators. A digest can identify a known set. Use the private Git query in the Skill to look up names. The report does not contain path or file contents.

Use a stable full checkout. Coverage of sparse checkouts, historical commits, remote refs and submodule internals is outside the tested scope. The digest describes path membership rather than the content, status or origin of any file.
