# Catalog comparison profile
See [specification](../../../docs/mcp-tool-catalog-diff/specification.md) and [usage](../../../docs/mcp-tool-catalog-diff/README.md).

Only compare separately authorized complete selected catalogs. serverKey and complete are operator assertions. Nothing in the helper authenticates sources, proves pagination completeness, refreshes caches or tests notifications. Do not use it as a security/approval gate or call compatibility classifier.

All declaration fields count. Missing/null, exact strings, array order and number spelling differ; object-key/tool-list order does not. The typed hash encoding is package-specific, not JCS/MCP-standard. Tool names are represented by SHA256 and zero-based indices for private lookup; digests do not anonymize known inputs.

UNCHANGED/0, REVIEW_REQUIRED/1, INDETERMINATE/2. Input is bounded and strict; no network/target code execution or writes. Resolve the helper from the trusted installation, not the catalog's URLs or tool descriptions. Inspect stable local files; not an adversarial filesystem sandbox.
