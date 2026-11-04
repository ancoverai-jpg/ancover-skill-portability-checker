# Source Archive Review — experimental
Review the actual source ZIP against explicit expected paths, without extracting or building it. The [Skill](../../skills/source-archive-review/SKILL.md) groups release review with the existing portability and CI tools. See [profile](../../skills/source-archive-review/references/profile.md), [specification](specification.md) and [validation](validation.md).

Requires Python3.10+; no pip packages. From repository root:
```sh
python -B examples/source-archive-review/make_demo.py archive-demo
python -B skills/source-archive-review/scripts/check.py archive-demo/expectations.json archive-demo/source.zip
```
The generator creates a new directory and refuses to overwrite it. The review intentionally exits1 for missing source and empty vendor prefix.
Install the Skill folder under .agents/skills for Codex or .claude/skills for Claude Code, or use the existing package plugin. Review diffs before replacing the installed folder; uninstall only that folder. Host conversation and Claude runtime coverage are separate.
Limitations:16MiB ZIP, stored/deflate, metadata and small-entry inspection only. No automatic root stripping, full payload CRC check, signature/provenance check, build, secret scan or LFS download. No finding means only the supplied checks were satisfied. Member names and artifact hash remain visible.
MIT license inherited from repository. Never attach credentials/private source to public issues; use private vulnerability reporting for sensitive reports. Contributions must preserve limits, fixed errors and no extraction. Changelog: experimental0.3.0 adds source-archive-review. Roadmap: collect real prerequisite policies before expanding formats; TAR support is out of scope.
