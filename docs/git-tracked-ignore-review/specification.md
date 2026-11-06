# Git Tracked Ignore Review

The operator selects a trusted, ordinary Git worktree root. The helper asks Git for current index paths matching repository .gitignore rules, including per-directory rules, and returns the unique match count and SHA256 of byte-sorted, NUL-terminated paths. Root selection overrides, Git diagnostics and unavailable inputs produce INDETERMINATE. The same Git rules power the optional private investigation.

Exit 0 means NO_INDEX_MATCHES under this profile. Exit 1 means INDEX_MATCHES and calls for operator review. Exit 2 means INDETERMINATE. A match can represent intentional indexing. The digest identifies a path set and is suitable for comparing reports from the same scope. It can identify a known set of paths.

The index includes staged paths, including an unborn branch. Git uses the repository rule files available during the inspection. Local .git/info/exclude and global exclusions belong to a separate scope. The profile covers the selected worktree and current index. Past commits, remote refs, file contents and submodule internals require separate inspection.

Run from a trusted package directory with an operator-trusted Git on PATH. The helper launches Git with fixed read commands, optional index writes disabled, and prompts and lazy fetching disabled. Use a stable worktree. Git commands have a ten-second timeout each and accept up to 1 MiB of captured output per command. The capture is held in memory before the limit check.

Acceptance covers actual Git index queries, root selection, tracked and untracked cases, nested rules and negation, local exclusion scope, invalid inputs, path suppression, read preservation, installation and CI. Host conversation tests, Claude runtime and sparse worktrees are recorded separately.
