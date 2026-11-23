# Decisions log (discovery notes, transcript, engagement artifacts)

Sources: Navex_Notes_15_OCT_2026.txt (Notes 15 Oct, Lnnn = line), Navex_VoC_Meeting_Transcript.txt (Transcript, mm:ss), Skill_Notes_Worked_Out.txt (Skill notes 19 Nov), Artifacts/NAVEX_VoC_Mockup_React_Handover.md (Handover md 16 Nov), engagement zip text files: Consolidated feedback 13 Nov, Response to technical questions 13 Nov (Tech answers), Enterpret integration notes 13 Nov, Tech stack detail 13 Nov, SSO and access 3 Nov, Platform swap 3 Nov, 00_INDEX 16 Nov; mockups Dec8, MVP v1, Latest Feedback, Latest (19 Nov). Discovery_Notes.txt holds generic consulting playbook research and no VoC decision.

Scope: decisions NOT already recorded in `docs/02-architecture/decisions.md`. Architecture decisions 1 to 15 live there; product rules live in `docs/01-product/requirements.md`, "Sources and precedence" and "Removed from the MVP". This file adds the dated trail and the who.

Rule: when two entries conflict, the later date wins. "Proposed" means a vendor (Psiog) recommendation that NAVEX has not confirmed.

## Business and scope decisions

| Date | Decision | Who decided (role) | Source |
|---|---|---|---|
| 2026-10 (call) | VoC becomes an enterprise, self-service capability with role-based access; adoption is the key success factor; first iteration serves customer experience (CX) staff looking at friction on their own accounts | NAVEX VoC lead, Product (Lindsay) | Transcript 1:00-1:58 |
| 2026-10 (call) | Engagement is not a competitive RFP; the vendor does the work; a gap assessment and proposal come back within about a week | NAVEX sponsor (role not stated) | Transcript 39:51-40:30 |
| 2026-10 (call) | Sentiment never stored in Snowflake (CAB sessions, council notes) needs its own repository; later became the knowledge hub | NAVEX VoC lead, Product | Transcript 38:35-38:59; Notes 15 Oct L378-386 |
| 2026-10 (call) | Write-back of insights goes to Snowflake, from which Gainsight or Salesforce pull it | NAVEX VoC lead, Product | Transcript 39:19. Superseded, see 2026-11-13 write-back row |
| Before 2026-10 (as-is) | All VoC channels centralised into Enterpret as the single feedback tool and taxonomy | NAVEX CSO office and Product | Notes 15 Oct L301-305 |
| As-is | Raw Enterpret dashboard access stays restricted | NAVEX VoC team | Notes 15 Oct L335 |
| As-is | Taxonomy gaps go to a Miscellaneous category; taxonomy is reviewed manually each quarter and can be re-run on history | NAVEX VoC team | Notes 15 Oct L359-360 |
| 2026-10-15 | The existing churn model is not merged into VoC scoring; churn score stays a separate measure | NAVEX VoC lead | Notes 15 Oct L393 |
| 2026-10-15 | VoC score and Gainsight score may show side by side but must not confuse the CXM | NAVEX VoC lead | Notes 15 Oct L447 |
| 2026-10-15 | Product roadmap tool (Aha!) is read only: pull from it, link the product monthly report into it | NAVEX Product | Notes 15 Oct L459-462 |
| 2026-10-15 | CXM experience is the MVP; Product (friction report for red and yellow domains, deep dives) is Phase 1 | NAVEX VoC lead | Notes 15 Oct L510-514 |
| 2026-10-15 | Access intent: CXM consumes own accounts and briefs; CXM leadership views and saves views, no contributor rights; Product is viewer and consumer; admins audit and approve | NAVEX VoC lead | Notes 15 Oct L522-529 |
| 2026-10-15 | Scope list is signed off by NAVEX before it is vetted further | NAVEX VoC lead | Notes 15 Oct L534 |
| 2026-10-15 | Scoring skills exclude call transcripts; use product ideas and CSAT only | NAVEX VoC lead | Notes 15 Oct L549-550 |
| 2026-11-13 | MVP = parity with the current At-Risk Account Scorecard; one view; no net-new feature without sign-off; keep/hold/remove table for added features | NAVEX CSO and project lead, with VoC SMEs | See `docs/reference/navex-mockup-feedback-2026-11-13.md` (whole file) |
| 2026-11-13 | VoC CTA in Gainsight is built by NAVEX, not by the platform | NAVEX VoC SME | `docs/reference/navex-mockup-feedback-2026-11-13.md`, User workflow |
| 2026-11-16 | Later-phase screens are proposals only, traced to the Phase 1 and Target State scope workbook | Psiog (proposed) | Handover md s2, s6 |
| 2026-11-19 | ELT viewer, Sales (AE) and Sales leadership sign in but get a "Yet to decide the modules and features" page | Psiog prototype, pending NAVEX | Latest prototype; see `docs/01-product/open-items.md` #4 |
| 2026-11-19 | Knowledge hub is admin-only, files publish straight away after checks | Psiog prototype, pending NAVEX | Latest prototype; see `docs/01-product/open-items.md` #1 |

## Technical decisions and proposals

| Date | Decision | Who decided (role) | Source |
|---|---|---|---|
| 2026-11-03 | Data platform sits behind ports; a swap (for example to Databricks) is a new adapter plus config plus the conformance suite, then re-baselined evaluation | Psiog (proposed) | Platform swap 3 Nov |
| 2026-11-03 | Out-of-scope reads return 404, same as missing; scope resolved once per request and bound into the statement | Psiog | SSO and access 3 Nov, Four rules. Now in `docs/01-product/roles-and-access.md`, Data scopes |
| 2026-11-03 | Scope cache 5 minutes (subject plus groups hash); ownership master cached 5 minutes; token never cached or logged | Psiog (proposed) | SSO and access 3 Nov, Caching |
| 2026-11-03 | Worker runs with its own workload identity at platform scope; every human read goes back through user scope | Psiog | SSO and access 3 Nov |
| 2026-11-13 | Backend is Python 3.13 and FastAPI; the 3 Nov scaffold also carried a .NET option, now dropped | Psiog, accepted in the build | Tech stack 13 Nov; Skill notes 19 Nov; Platform swap 3 Nov |
| 2026-11-13 | PostgreSQL (RDS) over DynamoDB for portability, about 47 USD a month more in production | Psiog | Tech stack 13 Nov, Platform |
| 2026-11-13 | CI type gate stays on mypy; the ty checker is local-only until stable | Psiog | Tech stack 13 Nov |
| 2026-11-13 | Observability: OpenTelemetry to Dynatrace; CloudWatch kept for AWS alarms | Psiog | Tech stack 13 Nov. Pointer: `docs/02-architecture/hld.md` |
| 2026-11-13 | Enterpret access by Bearer token (not OAuth) held in Secrets Manager, finite expiry (target six months), named rotation owner | Psiog (proposed) | Enterpret notes 13 Nov, Token handling |
| 2026-11-13 | Pull Enterpret as bulk deltas (watermark), never per account; refresh frequency then barely changes call volume | Psiog | Tech answers Q1 |
| 2026-11-13 | Refresh up to three times a day for freshness; evaluate and send alerts once a day; confirm count, dead band, cool-down | Psiog (proposed) | Tech answers Q1-Q2. Pointer: `docs/02-architecture/lld.md` 5.2 |
| 2026-11-13 | Use Entra app roles rather than raw group claims (groups claim drops above about 200 groups) | Psiog (proposed) | Tech answers Q3; SSO and access 3 Nov |
| 2026-11-13 | Gainsight: deep links for the MVP; iframe embedding not in MVP, assess in Phase 1 | Psiog (proposed) | Tech answers Q4 |
| 2026-11-13 | Write-back is Phase 1, direct to Gainsight API and Salesforce connected app, through an outbox with idempotency keys; Gainsight and Salesforce stay system of record for action state | Psiog (proposed) | Tech answers Q5. Supersedes the Snowflake write-back row |
| 2026-11-13 | Account-to-theme model is many to many; one primary theme per table column, proposed as highest negative volume | Psiog (proposed), NAVEX to confirm | Tech answers Q6. Pointer: `docs/02-architecture/lld.md` 5.4 |
| 2026-11-16 | Mockup state that defines a view (filters, sort, view) becomes URL search params, shared by saved views and deep links | Psiog | Handover md s1 |
| 2026-11-19 | Front-end stack, folder layout, five roles and four scopes, AWS SSO profiles in us-west-2 | Psiog skills | Skill notes 19 Nov. Pointer: `docs/03-engineering/coding-standards.md` |

## Superseded decisions (later wins)

| Earlier | Later | Winner |
|---|---|---|
| Next renewal date as a key landing measure (Notes 15 Oct L536) | Tile removed, date kept per account (Feedback 13 Nov) | Feedback 13 Nov |
| Admin library accepts call recordings, Teams recordings, PDF, Word, CSV, Excel (Notes 15 Oct L382-386) | pdf, docx, csv, xlsx, pptx, max 25 MB (Latest 19 Nov) | Latest |
| One theme per account (MVP v1 mockup) | Multiple Enterpret theme chips (Feedback 13 Nov, Tech answers Q6) | Feedback |
| Write-back via Snowflake (Transcript 39:19) | Direct Gainsight and Salesforce write-back, Phase 1 (Tech answers Q5) | Tech answers, still proposed |
| Knowledge hub deferred to later phases (Handover md, traceability) | Admin knowledge hub in the MVP (Latest 19 Nov) | Latest |
| Default sort ARR highest first; renewal window 90/180/365 days (Handover md s3) | Red with churn language first, then ARR; window within or beyond 180 days (Latest) | Latest |
| Five-tier adaptive taxonomy (Notes 15 Oct L177) | Three-level taxonomy cached per run (Enterpret notes 13 Nov) | Enterpret notes; confirm against the live schema |
| Verbatims fetched at view time, not stored (Enterpret notes 13 Nov 12:04) | Driver verbatims fetched each run for changed themes and stored masked (LLD v0.3, 13 Nov 12:24) | LLD, as in `docs/02-architecture/lld.md` 4.2 |

## Conflicts with docs/

| Topic | Sources say | docs/ says |
|---|---|---|
| CXM leadership upload | No contributor rights for leadership (Notes 15 Oct L525) | LLD lets leadership upload (`docs/02-architecture/lld.md` 2.1, 2.4); open item #1 leaves it open |
| Group claims | Recommend app roles, warn on group overflow (Tech answers Q3; SSO and access 3 Nov) | Keys may be app roles or group object IDs, NAVEX IT to confirm; no overflow handling named (`docs/01-product/roles-and-access.md`, Mapping Corp AD to roles) |
| Gainsight embedding | Not MVP, assess in Phase 1 (Tech answers Q4) | Not mentioned; only deep link (`docs/02-architecture/lld.md` 4.5) |
| Revocation delay | Scope cache 5 minutes sets the revocation delay (SSO and access 3 Nov) | No cache window stated in docs/ |
