# Ancover MCP Structured Result Check — specification
Experimental, legacy MCP 2025-06-18 / JSON Schema 2020-12 profile. This is a selected offline payload review, not a complete MCP conformance test or compatibility certification for modern protocol eras.

Audience: maintainers diagnosing whether a recorded structured result matches the selected tool outputSchema across a client/proxy boundary. Existing Inspector and SDK validators remain preferred for live transport integration. Added value is a bounded, value-suppressing local report, with explicit failure/unknown distinctions and paired upstream/downstream review instructions.

Inputs: a <=1 MiB UTF-8 JSON snapshot, explicit profile, selected tool declaration and selected CallToolResult (not JSON-RPC envelope). Strict JSON, <=12000 value nodes, depth<=48. No automatic selection, text-to-JSON recovery, network access, extraction or tool calls. Python3.12+ with six pinned wheel-only dependencies. No optional format extras.

Outputs: MATCH, MISMATCH, TOOL_ERROR, NOT_APPLICABLE, INDETERMINATE; sanitized reason code and snapshot SHA256. Exit0 only MATCH. Missing structured object is mismatch. isError:true always tool failure; no schema-success conclusion. Schema missing not applicable, unsupported dialect/references/invalid schema unknown. Validate only structuredContent; content text never substitutes. Local fragment refs supported; remote refs, custom vocabularies and alternate dialects conservative unknown. No format assertions, no default/coercion, unknown keywords follow library annotation behavior.

Bounds: trusted helper worker subprocess with five-second deadline; no custom reference retrieval. Input bounds do not constitute an OS memory sandbox. On timeout or any unresolved library condition return INDETERMINATE, suppress raw validator messages. No payload/field names/local paths in reports. Snapshot hashes can identify known inputs; treat reports accordingly.

Acceptance: envelope-versus-payload regression; missing object; tool errors; wrong types/required/additionalProperties/arrays/composition/local refs; remote refs fail closed; invalid/malformed/duplicate/oversize/deep inputs; no secret values in reports; deterministic synthetic sample; isolated installation; Windows/Ubuntu CI exact commit; Codex lifecycle installed helper; unavailable conversational and Claude coverage NOT_TESTED.
