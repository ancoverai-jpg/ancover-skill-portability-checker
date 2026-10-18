# Quality matrix

Reference inspected: [REA Portuguese README](https://github.com/morluto/rea/blob/main/docs/readme/README_pt-BR.md), [installer](https://github.com/morluto/rea/blob/main/install.sh), [contribution guide](https://github.com/morluto/rea/blob/main/CONTRIBUTING.md), [testing guide](https://github.com/morluto/rea/blob/main/docs/testing.md), [advertised example tests](https://github.com/morluto/rea/blob/main/src/contracts/advertisedInputExamples.test.ts), [installation failure tests](https://github.com/morluto/rea/blob/main/src/application/SetupInstallFailure.test.ts), package manifest and MIT license. Read-only inspection on 2026-10-17; its tests were not executed here.

REA connects a clear task to installation, examples and test contracts. Its installer guards truncated downloads and constrains version input. Contribution guidance asks for focused, justified changes and unavailable coverage. The applicable lesson is traceable claims with explicit boundaries. No REA implementation, prose or assets were copied.

| Criterion | Ancover acceptance evidence | Current artifact or gap |
|---|---|---|
|Problem and audience|Task, affected maintainer and primary reports|research.md; demand qualified only for pilot|
|Concrete value|Observable input/output and comparison|JSON preflight and seeded baseline; no adoption claim|
|Reproducible install|Frozen dependency installation in isolation|pnpm lock and clean-copy run|
|Executable examples|Run documented commands and capture outcomes|validation.md and demo artifacts|
|Use cases with evidence|Separate public report, static check and execution|Explicit evidence labels|
|Requirements/compatibility|Versions and host-specific matrix|Node/pnpm recorded; runtime host gaps explicit|
|Understandable architecture|Canonical content, adapters and bounded scripts|README architecture and source|
|Limitations/errors|Invalid target, malformed metadata, missing dependencies|Exit codes and negative cases|
|Update/uninstall|Isolated host lifecycle; no config loss|Host lifecycle procedure; pending coverage shown|
|Contribution/security/license|Policies, license and exact release review|Root policy files, MIT, lockfile|
|Maintenance|State, locks, demand gates and release cap|program.mjs and operations.md|

Stable publication requires closing host behavior and trigger evaluation gaps. An experimental label may disclose unavailable-host testing; it does not excuse failing supported behavior or secret exposure.
