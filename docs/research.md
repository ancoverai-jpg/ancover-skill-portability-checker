# Research and editorial ranking

Research date: 2026-10-17 (America/Sao_Paulo). Retrieval timestamps in JSON use UTC. Eight-niche exploratory sample, not a market-size estimate. Search queries and result dates are in `research-data.json`. Search matches were reviewed for relevance; broad matches are leads, not independent proof of a single opportunity. No stars, popularity metrics, quotes or customer claims used. Reports have not been independently reproduced.

## Developer experience

Audience: maintainers and platform teams. Candidate: **Windows environment recovery**.

uv handles installation; a recovery Skill must add diagnosis rather than wrap install commands.

Effort and risks: 1–2 weeks; platform support cost high. Enterprise relevance: repeatable onboarding, review and maintenance. Initial confidence: medium; all except the selected agent portability pilot remain hypotheses until three independent reports in two communities support the same task.

- [`uv python install` does not repair a managed installation whose interpreter executable is missing](https://github.com/astral-sh/uv/issues/22649) — opened 2026-10-16, updated 2026-10-16, open; author alex-feel.
- [uv installs x86_64 Python on arm64 Windows ](https://github.com/astral-sh/uv/issues/12906) — opened 2025-04-15, updated 2026-10-16, closed; author burgholzer.
- [Windows: uv pip install --overrides fails when requirements file path contains spaces](https://github.com/astral-sh/uv/issues/21477) — opened 2026-09-04, updated 2026-10-16, closed; author damonlynch.

## Testing and quality

Audience: maintainers and platform teams. Candidate: **Flaky CI evidence triage**.

Playwright traces and JUnit already exist; focus on separating flakiness from regressions.

Effort and risks: 1–2 weeks; reporter versions change. Enterprise relevance: repeatable onboarding, review and maintenance. Initial confidence: low; all except the selected agent portability pilot remain hypotheses until three independent reports in two communities support the same task.

- [Feature: Playwright's JUnit XML reporter annotate flaky tests.](https://github.com/microsoft/playwright/issues/35592) — opened 2025-04-13, updated 2026-10-16, closed; author avinashpoptani.
- [Regression 1.62.1 → 1.63.0: page Response.body() returns empty after in-page fetch().blob() already consumed it](https://github.com/microsoft/playwright/issues/42862) — opened 2026-09-22, updated 2026-10-15, open; author rusackas.
- [Bug: APIRequestContext ignores the server's Keep-Alive timeout, producing ECONNRESET on socket reuse](https://github.com/microsoft/playwright/issues/42698) — opened 2026-09-13, updated 2026-10-13, closed; author nick-vogel.

## Supply-chain security

Audience: maintainers and platform teams. Candidate: **Explain static score evidence**.

Scorecard is mature; avoid competing with its scanner or presenting scores as safety.

Effort and risks: 1–2 weeks; rule maintenance high. Enterprise relevance: repeatable onboarding, review and maintenance. Initial confidence: medium; all except the selected agent portability pilot remain hypotheses until three independent reports in two communities support the same task.

- [Enhancement of maintained check to better indicate abandoned repositories](https://github.com/ossf/scorecard/issues/5315) — opened 2026-10-12, updated 2026-10-15, open; author FelixOliverLange.
- [Feature - Pinned-Dependencies support self-repository GitHub actions syntax](https://github.com/ossf/scorecard/issues/5232) — opened 2026-09-10, updated 2026-09-28, closed; author Kielek.
- [Feature: Packaging check should detect winget publishing workflows](https://github.com/ossf/scorecard/issues/5168) — opened 2026-08-09, updated 2026-09-24, open; author mangokingTW.

## DevOps and infrastructure

Audience: maintainers and platform teams. Candidate: **Environment contract diagnosis**.

Compose config and env_file exist; redact values and diagnose precedence without exposing secrets.

Effort and risks: 1 week; parser semantics matter. Enterprise relevance: repeatable onboarding, review and maintenance. Initial confidence: medium; all except the selected agent portability pilot remain hypotheses until three independent reports in two communities support the same task.

- [FEATURE Declare sensitive variables and redact config output by default](https://github.com/docker/compose/issues/14356) — opened 2026-10-17, updated 2026-10-17, open; author savinmikhail.
- [BUG pre_start no longer inherits its parent environment](https://github.com/docker/compose/issues/14287) — opened 2026-10-06, updated 2026-10-12, closed; author JoaoLockem.
- [allow optional env_file for include top level](https://github.com/docker/compose/issues/13719) — opened 2026-04-07, updated 2026-10-07, open; author Dialgatrainer02.

## Data and databases

Audience: maintainers and platform teams. Candidate: **Migration drift investigation**.

Prisma already has migration diagnostics; destructive reset must not be the default remedy.

Effort and risks: 2 weeks; multiple DB engines and data risk. Enterprise relevance: repeatable onboarding, review and maintenance. Initial confidence: low; all except the selected agent portability pilot remain hypotheses until three independent reports in two communities support the same task.

The REST search returned HTTP 422. Follow-up primary discussions: [Prisma #23868, 2024-04-19](https://github.com/prisma/prisma/discussions/23868) and [Prisma #20025, 2023-06-30](https://github.com/prisma/prisma/discussions/20025). Historical evidence from one community; qualification is not met. Consequence: migration investigation can lead to destructive recovery choices.


## Integrations and APIs

Audience: maintainers and platform teams. Candidate: **MCP permission inventory**.

Official MCP documentation and scanners exist; separate declarations from observed calls.

Effort and risks: 2 weeks; authentication and untrusted server output. Enterprise relevance: repeatable onboarding, review and maintenance. Initial confidence: medium; all except the selected agent portability pilot remain hypotheses until three independent reports in two communities support the same task.

- [Security Advisory: SSRF, Indirect Prompt Injection, and sandbox bypass in @modelcontextprotocol/server-puppeteer](https://github.com/modelcontextprotocol/servers/issues/3662) — opened 2026-03-21, updated 2026-10-17, closed; author joergmichno.
- [🚨 Security Warning for MCP Server Developers and Users: Systematic Forking as a Supply-Chain Attack Vector](https://github.com/modelcontextprotocol/servers/issues/3635) — opened 2026-03-18, updated 2026-10-17, closed; author CSCSoftware.
- [server-everything: get-env returns the full process environment to the client (credential exposure)](https://github.com/modelcontextprotocol/servers/issues/4882) — opened 2026-09-27, updated 2026-09-28, open; author CieveMe.

## Documentation and maintenance

Audience: maintainers and platform teams. Candidate: **Release evidence handoff**.

MkDocs and link checkers exist; a report tying examples to observed commands may add value.

Effort and risks: 1 week; external links can be unstable. Enterprise relevance: repeatable onboarding, review and maintenance. Initial confidence: low; all except the selected agent portability pilot remain hypotheses until three independent reports in two communities support the same task.

- [Enable users to change log level](https://github.com/mkdocs/mkdocs/issues/2876) — opened 2022-07-01, updated 2026-03-09, closed; author AngryMane.
- [False positive `relative_to_docs` absolute path validation warning](https://github.com/mkdocs/mkdocs/issues/3589) — opened 2024-03-05, updated 2026-03-09, closed; author Blacksmoke16.
- [Header and navigation sidebars display incorrectly arbitrary markup](https://github.com/mkdocs/mkdocs/issues/3357) — opened 2023-08-28, updated 2026-03-09, closed; author Enn83.

## Agent workflows and interoperability

Audience: maintainers and platform teams. Candidate: **Skill preflight across hosts**.

skills-ref validates the standard; host validators test their own formats. Add a conservative multi-manifest report with exact content digest, without replacing either.

Effort and risks: 3–5 days initial pilot; host drift is ongoing. Enterprise relevance: repeatable onboarding, review and maintenance. Initial confidence: medium; all except the selected agent portability pilot remain hypotheses until three independent reports in two communities support the same task.

- [MCP server processes leak: per-thread processes never cleaned up (9+ GB RSS)](https://github.com/openai/codex/issues/30408) — opened 2026-06-28, updated 2026-10-17, open; author kkkayye.
- [Windows dot-started local tasks lack Computer Use tools while ordinary local Codex sessions work](https://github.com/openai/codex/issues/49458) — opened 2026-09-30, updated 2026-10-17, open; author gaopengbin.
- [ChatGPT Desktop: local MCP tools are discovered successfully but not exposed to Chat sessions](https://github.com/openai/codex/issues/38162) — opened 2026-08-12, updated 2026-10-17, open; author brad8898.

## Selected pilot: evidence qualification

The following three reports have different authors and come from three project communities. They concern metadata acceptance and portability. They are not duplicate reposts based on their distinct reproductions; this is an editorial independence assessment. Some are closed: the demand evidence is historical, not a claim those defects remain. The narrower gap to test is one review artifact across package overlays and exact content, rather than a new YAML standard validator. Confidence is medium until user adoption feedback.

- [Codex App skips loading curated plugin skills due to metadata validation limits](https://github.com/openai/codex/issues/25996) — openai/codex, Lesterffx, opened 2026-06-03, closed. 
- [SKILL.md frontmatter uses flow sequences which fail `agentskills validate`](https://github.com/googleworkspace/cli/issues/521) — googleworkspace/cli, ytausch, opened 2026-03-17, closed. 
- [Plugin skill with a namespaced frontmatter `name` gets the plugin prefix applied twice (2.1.216)](https://github.com/anthropics/claude-code/issues/80631) — anthropics/claude-code, cameronsjo, opened 2026-07-23, open. 
- [Spec lacks guidance on skill verification and supply-chain trust](https://github.com/agentskills/agentskills/issues/418) — agentskills/agentskills, theyavuzarslan, opened 2026-06-09, closed. Additional supply-chain context; not counted toward the three metadata reports.

Existing alternatives: [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) validates standard metadata; [Claude plugin tooling](https://code.claude.com/docs/en/plugins) validates and loads Claude packages; [Codex plugin guidance](https://developers.openai.com/plugins/build/plugins) defines packaging. The pilot deliberately adds a small local report and does not claim full equivalence or superior coverage. No new MCP server is needed.

## Editorial scores

Each dimension is 1–5, equally weighted; total is the sum (maximum 45). These are judgments, not measurements. Dimensions: pain, evidence, alternative gap, demonstrable value, adoption, Skill fit, enterprise relevance, maintenance feasibility, Ancover fit. Qualification overrides total.

| Rank | Opportunity | Scores in dimension order | Total | Decision |
|---|---|---|---|---|
|1|Skill preflight|4,4,2,4,4,5,4,4,5|36|Demand qualified; build one experimental pilot|
|2|Release evidence handoff|3,2,2,4,4,5,4,4,5|33|Specify; demand hypothesis|
|3|Environment contract diagnosis|4,2,2,4,3,4,5,3,4|31|Specify; demand hypothesis|
|4|MCP permission inventory|4,2,2,4,3,4,5,2,5|31|Research; server trust risk|
|5|Static score explanation|3,2,1,3,4,5,4,3,5|30|Research; avoid scanner duplication|
|6|Flaky CI triage|4,2,2,4,3,4,4,2,3|28|Research; crowded alternatives|
|7|Windows recovery|4,2,2,4,3,4,3,2,3|27|Research; platform support burden|
|8|Migration drift investigation|5,2,1,4,2,3,5,1,3|26|Research; data risk and existing tools|

Pain scores reflect consequences in the linked reports; evidence discounts single-community samples and historical fixes; gap discounts existing validators; value scores favor deterministic outputs; adoption discounts setup and credentials; fit favors bounded repeatable Skills; enterprise relevance favors reviewability; maintenance discounts fast-changing host/database behavior; Ancover fit favors evidence and capability evaluation. Ties favor lower maintenance risk. No repository splits until distinct product/audience/release cadence is demonstrated.
