# Ancover MCP Tool Catalog Diff
Experimental offline comparison of two selected complete MCP-style tool catalogs. [Skill](../../skills/mcp-tool-catalog-diff/SKILL.md) · [Research](research.md) · [Specification](specification.md) · [Português](README.pt-BR.md)

Requires Python3.12+ standard library. No additional dependency installation. Clone/download this trusted package, then:
```sh
python -I -B skills/mcp-tool-catalog-diff/scripts/compare.py examples/catalog-before.json examples/catalog-after.json
```
The synthetic example returns REVIEW_REQUIRED/exit1 because the same tool name now declares a required revision parameter. Compare before.json with itself for UNCHANGED/0. Wrong/missing inputs return INDETERMINATE/2. These are actual comparison outcomes, not real server/tool execution evidence.

Each selected file must contain profile=ancover-mcp-tool-catalog-v1, the same serverKey, complete=true, and tools. Each tool needs a unique nonempty case-sensitive name and object inputSchema. Capture all pages separately, preserve acquisition origin/time/revision/protocol, and omit nextCursor only after the catalog is actually complete. No envelope unwrapping or automatic capture is performed. A complete flag is not independently verified.

The comparison includes all tool declaration fields, including unknown fields as other. Object keys and top-level tool order do not affect equality. Strings, array order, null versus absence and exact JSON number spelling are retained. Large numbers are not rounded to floats. For example1,1.0 and1e0 conservatively differ; required-array reorder also differs. Root capture metadata is excluded from tool equality. This application-specific tagged representation is NOT JCS/RFC8785, JSON Schema semantic equivalence or an interoperable MCP fingerprint.

Bounds:1MiB per regular UTF-8 file,256 tools,12000 value nodes, depth48,128-character number lexemes,256-character names and128-character serverKey. Duplicate JSON keys, duplicate names, non-JSON constants, pagination fields and mismatched scope fail closed. Use stable local files; resource limits are not an OS sandbox or protection from concurrent filesystem changes.

Reports contain fixed categories, counts, zero-based beforeIndex/afterIndex and SHA256 tool-name/file digests, never raw tool names, definitions, field values or local paths. Indices let reviewers find declarations privately. Digests can identify known inputs; value suppression is not anonymization. Nothing is uploaded; no schema URL is followed. The comparator cannot detect malicious behavior with unchanged declarations.

Installation/update/removal: use the complete package's isolated plugin lifecycle, retaining its referenced docs layout. Standalone Skill-only distribution is NOT_TESTED. Review diff before replacing only the selected installation; rerun the example. Remove only that installation. No global packages or personal settings are changed by the helper. The package's older helpers retain their own existing pinned dependencies; this new helper does not import them.

See [validation](validation.md). Codex helper/lifecycle evidence and conversational trigger behavior are separate; conversation and Claude runtime remain NOT_TESTED where unavailable. MIT package; no copied third-party code, no new dependency license. SECURITY.md and CONTRIBUTING.md apply.
