# Units of work

The MVP split into units a developer or an AI harness can take one at a time. Each unit names its requirements, where the code goes and how to tell it is finished. Requirement detail is in `docs/01-product/requirements.md`.

Status: **Done** is in this skeleton with tests. **Open** is ready to build. **Blocked** waits on the input shown.

## Definition of done for every unit

- Each "Done when" check of its requirements has a test or a recorded demo step.
- The quality gate passes: `ruff`, `mypy`, `pytest`, `tsc`, `eslint`, `vitest`, build.
- No blocker from `.harness-records/skills/navex-security-code-review`.
- Labels and messages match the latest prototype and pass a grammar review.
- The feature or service `README.md` and `docs/03-engineering/api-contract.md` are updated.

## Foundation

| Unit | Scope | Requirements | Code | Status |
|---|---|---|---|---|
| FND-01 | Repository, workspace, quality gate, CI workflow, editor settings | NFR-H | root, `.github`, `.vscode` | Done |
| FND-02 | Serving store schema, scope filter, baseline migration | AUT-07 | `packages/voc-data` | Done |
| FND-03 | Knowledge base and skills | | `docs`, `.harness-records/skills` | Done |
| FND-04 | Sample data for DEV and local use: accounts, people, one published run | | `packages/voc-data` (new seed script) | Open |
| FND-05 | Entra app registrations, role map, team access to GitHub and AWS | AUT-01 | `.env` values | Blocked: NAVEX IT |

## Experience API, `services/experience-api`

| Unit | Scope | Requirements | Code | Status |
|---|---|---|---|---|
| API-01 | Token verification, entitlements, scope, paging, errors, audit, telemetry | AUT-01 to AUT-05, AUT-07, ACC-15 | `app/core` | Done |
| API-02 | Accounts list and detail, portfolio summary, saved views | SCR-01, SCR-02, SCR-04 to SCR-06, ACC-01 to ACC-03, ACC-06 to ACC-08, ACC-14, SVW-01 to SVW-04 | `domains/accounts`, `portfolio`, `saved_views` | Done |
| API-03 | Week-over-week trend from weekly snapshots | SCR-07 | `domains/portfolio` | Open |
| API-04 | Excel export with audit; account brief | EXP-01, EXP-02, ACC-13 | `domains/accounts` | Open |
| API-05 | Notifications list and mark read | ALR-05, ALR-06 | `domains/notifications` | Open |
| API-06 | Manager summary, report templates, friction report | LDR-01 to LDR-05 | `domains/leadership` | Open; response fields blocked on open item 3 |
| API-07 | Admin home, weekly changes, email to leadership | ADM-01 to ADM-03 | `domains/admin` | Open |
| API-08 | Source health, refresh runs, usage, audit, access list, their exports | ADM-04 to ADM-09, EXP-03 | `domains/admin` | Open |
| API-09 | Knowledge hub: upload ticket, completion, file checks from the GuardDuty event, list, download, withdraw, approve, decline | KHB-01 to KHB-05 | `domains/knowledge_hub`, `ports/document_store.py` | Open; publication rule on open item 1 |
| API-10 | Digest schedules, configure, preview, send, archive, personal settings | DIG-01 to DIG-05, DIG-07 | `domains/digests` | Open |

## Web app, `apps/web`

| Unit | Scope | Requirements | Code | Status |
|---|---|---|---|---|
| WEB-01 | Sign-in, entitlements, permission guards, app shell with bell icon, loaders, theme | AUT-01 to AUT-04, AUT-09, KHB-06 | `features/auth`, `components`, `routes`, `styles` | Done |
| WEB-02 | Scorecard reference slice: header, refresh notice, rating cards, first filters, table | SCR-01, SCR-02, SCR-04, SCR-05, ACC-01 to ACC-03 | `features/accounts`, `features/themes` | Done |
| WEB-03 | AI notice; total ARR at risk by segment | SCR-03, SCR-06 | `features/accounts` | Open |
| WEB-04 | Week over week | SCR-07 | `features/accounts` | Open, after API-03 |
| WEB-05 | Full filter bar, paging, rule chip tooltips, taxonomy cell, card layout below 1024px | ACC-04 to ACC-06, ACC-15, NFR-C | `features/accounts` | Open |
| WEB-06 | Inline account detail, measures, verbatims, friction trend, deep link | ACC-07 to ACC-12, AUT-06, ALR-03 | `features/accounts`, `features/themes` | Open |
| WEB-07 | Saved views tab, Excel download, account brief dialog | SVW-01 to SVW-04, EXP-01, ACC-13 | `features/saved-views`, `features/accounts` | Open; brief after API-04 |
| WEB-08 | Notifications list behind the bell | ALR-05, ALR-06 | `features/notifications` | Open, after API-05 |
| WEB-09 | Manager summary | LDR-01 to LDR-03 | `features/leadership` | Open, after API-06 |
| WEB-10 | Custom reports and weekly friction report | LDR-04, LDR-05 | `features/leadership` | Open, after API-06 |
| WEB-11 | Admin home; weekly changes with the email form | ADM-01 to ADM-03 | `features/admin` | Open, after API-07 |
| WEB-12 | Data source health, refresh runs, usage and audit, access list | ADM-04 to ADM-09, EXP-03 | `features/admin` | Open, after API-08 |
| WEB-13 | Knowledge hub upload and list | KHB-01 to KHB-04 | `features/knowledge-hub` | Open, after API-09 |
| WEB-14 | Scheduled digests; personal digest settings | DIG-01 to DIG-05, DIG-07 | `features/digests` | Open, after API-10 |
| WEB-15 | Accessibility pass, copy and grammar pass, session timeout | NFR-B, NFR-G, AUT-08 | all features | Open |

## Ingestion task, `services/ingestion`

| Unit | Scope | Requirements | Code | Status |
|---|---|---|---|---|
| ING-00 | Pipeline, masking, matching, staging, hand-over to the agent | REF-01, REF-03, REF-04 | `pipeline.py`, `adapters/staging.py`, `adapters/agentcore.py` | Done |
| ING-01 | Snowflake view and column mapping | REF-02 | `adapters/snowflake.py` | Blocked: NAVEX data team, open item 10 |
| ING-02 | Enterpret taxonomy, counts and verbatims through MCP | REF-02 | `adapters/enterpret.py` | Blocked: Enterpret access and probe results, open item 18 |
| ING-03 | Retry with backoff; source health records | ADM-04, NFR-06 | `pipeline.py`, new source health table | Open |
| ING-04 | Org chart sync from Microsoft Graph into `person` | AUT-07, ADM-07 | new `adapters/graph.py` | Blocked: Graph permission, open item 12 |

## Account Scoring Agent, `services/account-scoring-agent`

| Unit | Scope | Requirements | Code | Status |
|---|---|---|---|---|
| AGT-00 | Graph, scoring rules interface, triggers, theme ranking, status confirmation, summary prompt, publish | REF-05 to REF-10, ALR-02, ACC-10 | `graphs`, `domain`, `prompts`, `tools` | Done |
| AGT-01 | NAVEX rule set and friction score in place of the placeholder | REF-05, ACC-04, ACC-12 | `domain/scoring.py`, `rules/` | Blocked: rule set from NAVEX, open item 9 |
| AGT-02 | Deploy to AgentCore Runtime in DEV; confirm the model ID | REF-07 | `entrypoint.py`, `Dockerfile` | Blocked: NAVEX IT |
| AGT-03 | Weekly cut-off and the alert evaluation flag | REF-09, ALR-01 | `tools/serving_store.py`, `graphs` | Open; cut-off on open item 11 |
| AGT-04 | Account brief and leadership weekly brief prompts | ACC-13, LDR-01 | `prompts`, `schemas` | Open |

## Notification task, `services/notifications`

| Unit | Scope | Requirements | Code | Status |
|---|---|---|---|---|
| NTF-01 | Change-of-status alerts, batched per owner, idempotent | ALR-01, ALR-04 | `alerts.py`, `templates` | Done |
| NTF-02 | Scheduled digests by audience | DIG-02, DIG-06 | new `digests.py` | Open |
| NTF-03 | Admin failure notices; knowledge hub decision emails | REF-10, KHB-04 | new modules | Open |
| NTF-04 | Email service adapter NAVEX approves | ALR-01 | `ports.py` | Blocked: open item 15 |

## Operations

| Unit | Scope | Requirements | Code | Status |
|---|---|---|---|---|
| OPS-01 | Deploy workflow from GitHub Actions to AWS with OIDC | | `.github/workflows` | Blocked: NAVEX IT deploy role |
| OPS-02 | OpenTelemetry to Dynatrace in all four services | NFR-F | `core/telemetry.py` | Open; API tracing is in place |
| OPS-03 | Performance check of the scorecard at full scope | NFR-D | | Open |

## Suggested order

| Wave | Goal | Units |
|---|---|---|
| 1 | A signed-in CXM sees their real accounts | FND-04, FND-05, ING-01, ING-02, AGT-01, AGT-02, WEB-03, WEB-05, WEB-06 |
| 2 | Parity and alerts | API-03, API-04, WEB-04, WEB-07, AGT-03, ING-03, ING-04, NTF-04, API-05, WEB-08 |
| 3 | Admin and leadership | API-07, API-08, WEB-11, WEB-12, API-10, NTF-02, WEB-14, API-09, WEB-13, API-06, WEB-09, WEB-10 |
| 4 | Hardening | WEB-15, OPS-01 to OPS-03, NTF-03, AGT-04 |

Waves 1 and 2 cover the five outcomes in NAVEX's definition of done. Units in wave 3 marked `Confirm` in the requirements wait for the NAVEX decision.
