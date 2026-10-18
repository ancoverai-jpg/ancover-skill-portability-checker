# Security

Version 0.1 is experimental. Review findings and source before use. The checker never executes target code, but is not a sandbox: inspect a stable snapshot in an isolated environment for hostile targets. Filename filters are not a secret scanner. The digest excludes Git, installed dependencies and runtime state; it is not signed. Reports may reveal local filenames. There is no telemetry.

Do not disclose secrets or exploitation details in public issues. Once the GitHub repository exists, enable GitHub private vulnerability reporting and use its Security tab for confidential reports. Until that is configured, no private reporting channel or response SLA is claimed. For public, non-sensitive defects, provide a minimal synthetic fixture. Dependencies are pinned by pnpm-lock.yaml; install with scripts disabled and review dependency updates before merging. The YAML parser declares ISC licensing; see [third-party notices](THIRD_PARTY_NOTICES.md).
