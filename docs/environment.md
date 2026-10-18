# Environment diagnosis — 2026-10-17

The starting workspace contained empty `work/` and `outputs/` directories, with no repository or local AGENTS.md at the inspected workspace and date-root levels. Existing Ancover application source was located separately and left unchanged; generated data, keys and logs were never read or packaged.

Verified tools: Windows PowerShell 7.6, Git, Node v24.19.0, bundled pnpm v11.25.0 and Codex CLI 0.163.0-alpha.10.2. `npm` and Claude Code were not on PATH. A bundled Python runtime is available for package inspection. The Windows Store python alias is not treated as an installed runtime.

The installed Ancover IA package is an App-backed personal private plugin, version 1.0.0 at inspection. Its source inventory contained only `.app.json` and `.codex-plugin/plugin.json`; there were no Skills. Exact backend identity and current release were retrieved through Plugin Creator. Its connection, presentation and audience must be preserved. The new research Skill is maintained canonically in this source and can be overlaid through the owning plugin release workflow. The open source package does not expose private App configuration.

Ancover tools actually called: `list_plugins` and `search_public_capabilities`. Both returned MCP -32603 Internal error. Tool schemas expose discovery, comparison, saved Skills, static evidence and simulations; those descriptions are not runtime verification. No Ancover runtime success, catalog emptiness or repair is claimed. Research used public primary sources as fallback. No production deployment was attempted.

GitHub connector authenticated profile: `ancoverai-jpg`. The user confirmed this destination. `list_installed_accounts` and `list_repositories` returned empty arrays. Thus no repository write access or create-repository capability was established. The exposed connector has file/branch/PR mutation tools but no repository-creation tool. `gh` was not found. No credentials were printed or extracted. Creating a new public repository remains pending a supported authorized creation path; existing private repositories will not be repurposed.

Scheduling mechanism: Codex thread heartbeat automation is exposed. It can resume this thread on the local host. Actual creation/status and conditions are recorded in operations.md; a file by itself does not establish an active schedule.

Final observed changes: the existing Ancover IA plugin was saved as 1.0.1 with portfolio-research added. Read-back verified unchanged App binding, presentation and identity. Codex local installation/removal and modified-version reinstall succeeded under an isolated CODEX_HOME. The GitHub browser fallback reached the sign-in screen; no authenticated repository-creation session was available. No repository was created.

Official sources inspected: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins), [Skill authoring](https://developers.openai.com/plugins/build/skills), [Claude plugins](https://code.claude.com/docs/en/plugins), [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [GitHub workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow). Formats were selected from those sources; this report does not infer installation success from manifest existence.
