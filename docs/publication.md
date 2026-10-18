# First experimental publication

Repository: [Ancover Skill Portability Checker](https://github.com/ancoverai-jpg/ancover-skill-portability-checker). Public source was created in the authenticated ancoverai-jpg account with explicit user authorization.

The GitHub integration could read repository metadata but its create-tree request returned 403 Resource not accessible by integration. The authenticated browser upload workflow published the reviewed source without changing App permissions or extracting credentials. This distinction matters for future maintenance: connector read access is verified; connector write remains unavailable until its integration permissions change. The browser session is a verified write path when authenticated.

Commit [d6d2534d3319844ed79830407ce0fbede77c6c17](https://github.com/ancoverai-jpg/ancover-skill-portability-checker/commit/d6d2534d3319844ed79830407ce0fbede77c6c17) contained all 33 planned source files. A fresh public Git clone compared every file byte-for-byte against the local source and found zero differences. Dependencies, runtime state, local logs and credentials were excluded.

[Validation run 39087680324](https://github.com/ancoverai-jpg/ancover-skill-portability-checker/actions/runs/39087680324) passed on Windows and Ubuntu using Node 22. Each job installed the frozen dependencies with install scripts disabled, executed 11 tests and ran static self-inspection. This is actual remote execution, not a configured-only workflow.

Private vulnerability reporting, dependency graph and Dependabot alerts were enabled through repository settings. Secret scanning and push protection were already enabled. Code scanning and paid AI security features were not claimed as active.

The initial release remains experimental. Conversational trigger behavior and Claude Code runtime coverage are NOT_TESTED. CLI tests and CI do not establish full host compatibility or security certification. This repository counts as one new project publication, not one project plus its bundled Skills. Documentation updates, commits and a release tag do not create additional daily publication units.

Earlier reports of zero accessible repositories describe the pre-creation state. The repository and source publication supersede that blocker; the integration-specific write restriction and host coverage gaps remain explicit.
