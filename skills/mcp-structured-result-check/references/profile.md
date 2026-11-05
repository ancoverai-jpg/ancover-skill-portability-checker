# Supported review profile
Read the package [specification](../../../docs/mcp-structured-result-check/specification.md) and [usage/limits](../../../docs/mcp-structured-result-check/README.md). All assumptions are explicit: legacy MCP2025-06-18, Draft2020-12, selected corresponding declaration/result, root object schema, format annotations only, local fragments only.

Only MATCH exits0. MISMATCH/TOOL_ERROR exit1; unknown/not applicable exit2. A match describes a supplied recorded object, not authenticated live execution or host conformance. For newer protocol eras use appropriate official SDK/Inspector behavior instead of changing the profile label.

Use a trusted helper path and isolated virtual environment. No target scripts are executed. Installation requires pinned dependencies and network package download; checking does not. Five-second worker termination bounds validation duration but not peak memory; use an OS sandbox for adversarial inputs. Never publish private snapshots merely because reports omit values.
