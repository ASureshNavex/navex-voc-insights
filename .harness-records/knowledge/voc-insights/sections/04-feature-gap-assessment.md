# 04 Feature gap assessment, use cases, solution paths
Sources: NAVEX_VoC_Features_Gap_Assessment_Usecases_Potential Solution Paths.xlsx (Oct 2026; sheets Summary, Gap matrix, Feature List, Use Cases, Decisions & risks, Solution Approach). The workbook marks itself provisional and pre-proposal. It predates the FRD and the Closure deck.

## Already in docs/ (read there, not here)

Nothing from this workbook is in `docs/`. The related current decisions are in:
- AI runtime and hosting: `docs/02-architecture/overview.md` (container table).
- Open decisions for NAVEX: `docs/01-product/open-items.md`.
Later sources settle some gaps below; see "Conflicts with docs/".

## Legend

- Milestone: MVP, P1 = Phase 1, TS = Target State, TBC = to confirm.
- Type: RFP = explicit in the RFP; NAVEX = stated by NAVEX (call, documents, diagram); Supp = supporting capability needed to deliver the stated ones; Scope? = mentioned, not agreed in scope.
- Gap dimensions: Data, Src (source connection), Rules (scoring), AI, App (application), Sec (access and security), Int (integration and outputs), Ops (operations), Gov (governance).
- Full = capability missing. Part = exists in part; extend or automate.

## Features (Gap xlsx, Summary)

| # | Feature | Module | # | Feature | Module |
|---|---|---|---|---|---|
| 1.1 | Account Risk Scoring | Account Intelligence | 3.1 | Curated Report Library | Reporting |
| 1.2 | Account Narratives | Account Intelligence | 3.2 | AE Account View | Reporting |
| 1.3 | CXM Account View | Account Intelligence | 4.1 | Source Connections | Data and Integration |
| 1.4 | CXM Leadership View | Account Intelligence | 4.2 | Knowledge Hub | Data and Integration |
| 2.1 | Product Domain Friction Report | Product Intelligence | 4.3 | Write-Back and Distribution | Data and Integration |
| 2.2 | Self-Serve Research | Product Intelligence | 5.1 | Access and Security | Platform Foundations |
| 2.3 | Fact Base Briefings | Product Intelligence | 5.2 | Rules, Skills and Templates | Platform Foundations |
| | | | 5.3 / 5.4 | Operations / Quality and Adoption | Platform Foundations |

Full gaps are concentrated in App (17 functions) and Ops (10). Governance is mostly "Unknown" (38 functions) (Gap xlsx, Summary).

## Functions (Gap xlsx, Gap matrix and Feature List)

| ID | Feat | Function | Milestone | Type | Full | Part | Decision needed |
|---|---|---|---|---|---|---|---|
| F-01 | 1.1 | Calculate account rating daily (RYGG rules, every in-scope account) | MVP | RFP | - | Data, Rules | Where scoring runs |
| F-02 | 1.1 | Apply signal windows (30-day signal, 90-day support-case) | MVP | NAVEX | - | Rules | - |
| F-03 | 1.1 | Record the rule behind each rating | MVP | Supp | - | Rules | Keep all rules met, or only the first? |
| F-04 | 1.1 | Confirm every account is scored (coverage check) | MVP | RFP | Ops | - | - |
| F-05 | 1.1 | Reconcile ratings with Snowflake | MVP | RFP | Ops | Rules | Source of truth: the Claude-skill or the Snowflake version |
| F-06 | 1.2 | Generate a narrative per at-risk account | MVP | RFP | - | Data, AI | AI platform (F-58) |
| F-07 | 1.2 | Summarise top themes | MVP | NAVEX | - | Data, AI | - |
| F-08 | 1.2 | Identify affected product or subscription | MVP | Supp | - | Data | Can feedback map to a subscription? |
| F-09 | 1.2 | Use approved knowledge context in narratives | MVP | NAVEX | Src, AI | - | Retrieval approach |
| F-10 | 1.2 | Link narrative to source records | MVP | NAVEX | - | AI | - |
| F-11 | 1.2 | Show verbatims on request, PII protected | MVP | NAVEX | - | - | What each role may see |
| F-12 | 1.3 | Show my accounts (CXM own book) | MVP | RFP | App | Data | Where CXMs work day to day |
| F-13 | 1.3 | Show rating, narrative and evidence | MVP | RFP | App | - | - |
| F-14 | 1.3 | Filter and sort accounts | MVP | NAVEX | - | Data, App | - |
| F-15 | 1.3 | Show ARR, renewal, CXM, AE, exec sponsor | MVP | NAVEX | - | Data, App | Master system per field |
| F-16 | 1.3 | Show NPS with survey date | MVP | NAVEX | - | Data, App | - |
| F-17 | 1.3 | Show open issues | MVP | NAVEX | Data, App | - | Ingestion timing |
| F-18 | 1.3 | Show churn prediction beside rating, kept separate | TBC | Scope? | App | - | Whether churn is shown in this view |
| F-19 | 1.3 | Record action taken | TBC | Scope? | - | - | In scope? Where actions are recorded today |
| F-20 | 1.4 | Show most friction-ridden accounts across a manager's teams | MVP | NAVEX | App | Data | Milestone (raised on a call, not in the RFP) |
| F-21 | 1.4 | Filter by CXM manager | MVP | NAVEX | App | Data | Hierarchy source |
| F-22 | 1.4 | Support escalation decisions (save desk, raise issue) | TBC | Scope? | - | - | In scope? |
| F-23 | 2.1 | Calculate domain ratings monthly | P1 | RFP | - | Data, Rules | Where domain logic runs |
| F-24 | 2.1 | Apply volume tiers and trend flag | P1 | NAVEX | - | Rules | - |
| F-25 | 2.1 | Summarise top themes per domain | P1 | NAVEX | - | AI | - |
| F-26 | 2.1 | Link themes to roadmap work (Aha!) | P1 | NAVEX | - | Data, AI | Matching method |
| F-27 | 2.1 | Break down by region and segment | P1 | NAVEX | - | Data | - |
| F-28 | 2.2 | Ask questions in plain language | P1 | RFP | App | AI | AI platform (F-58) |
| F-29 | 2.2 | Return evidence-backed answers | P1 | NAVEX | - | AI | - |
| F-30 | 2.2 | Use all approved sources | P1 | NAVEX | - | Src | Sources approved for the agent |
| F-31 | 2.3 | Produce on-demand briefings | TS | RFP | App | Src, AI | - |
| F-32 | 2.3 | Deliver automated Fact Base insights | TS | RFP | - | AI | Audience, cadence, channel |
| F-33 | 3.1 | Provide Product's ~6 regular reports | P1 | NAVEX | App | AI | Skill maturity |
| F-34 | 3.1 | Provide templated outputs (e.g. QBR briefs) | P1 | RFP | App | AI | - |
| F-35 | 3.1 | Provide ELT and business reports | P1 | RFP | App | - | Which reports are in scope |
| F-36 | 3.2 | Show AE's accounts | P1 | RFP | App | Data | What AEs need |
| F-37 | 4.1 | Maintain the Snowflake-Enterpret feed | MVP | NAVEX | - | - | Refresh frequency vs a daily MVP |
| F-38 | 4.1 | Provide Enterpret access to the platform | MVP | RFP | - | Src | Access method: Snowflake, API or MCP; licence |
| F-39 | 4.1 | Retrieve product, subscription, roadmap context | MVP/P1 | Supp | - | Data | Authoritative source per data type |
| F-40 | 4.1 | Check source freshness and completeness | MVP | Supp | Ops | Data | Owner of data exceptions |
| F-41 | 4.1 | Check account and product mapping | MVP | Supp | Ops | Data | Master identifiers |
| F-42 | 4.1 | Use Pendo and competitive intelligence | TS | RFP | - | - | Approved for agent use |
| F-43 | 4.1 | Add call transcripts | TBC | NAVEX | - | Src | Timing vs MVP |
| F-44 | 4.1 | Add further sources with little effort | P1 | NAVEX | - | Src | Approval path for new sources |
| F-45 | 4.2 | Upload non-standard sources (CAB notes, research) | MVP | RFP | Src, App | - | Volume and formats |
| F-46 | 4.2 | Approve content before use | MVP | RFP | App | - | Who approves |
| F-47 | 4.2 | Store outside Snowflake and Enterpret with access control | MVP | RFP | Src | - | Storage location |
| F-48 | 4.2 | Manage content ownership and versions | MVP | Supp | App | - | Ownership model |
| F-49 | 4.2 | Replace, retire or remove content | MVP | Supp | App | - | Review and retention policy |
| F-50 | 4.3 | Write ratings and narratives to Snowflake (history to confirm) | MVP | RFP | - | Int | Schema, history, update behaviour |
| F-51 | 4.3 | Feed Gainsight | MVP | RFP | - | Int | Fields, owner |
| F-52 | 4.3 | Feed Salesforce | MVP | RFP | - | - | Current route, fields, owner |
| F-53 | 4.3 | Feed Power BI | TBC | Scope? | - | Int | Whether in scope |
| F-54 | 4.3 | Confirm downstream delivery | MVP | Supp | Ops | - | Owner of delivery issues |
| F-55 | 5.1 | Maintain account ownership mapping (CXM, AE, manager, sponsor) | MVP | Supp | - | Data, Src | Owner of ownership data |
| F-56 | 5.1 | Enforce role-based visibility | MVP | RFP | Sec | - | Role definitions |
| F-57 | 5.1 | Protect PII in outputs | MVP | RFP | - | - | What counts as PII (written rules) |
| F-58 | 5.1 | Run AI within the approved boundary | MVP | NAVEX | - | - | Cortex only, or Claude directly |
| F-59 | 5.2 | Change and version scoring rules | MVP | NAVEX | Rules | Gov | Change approval (CSO governs) |
| F-60 | 5.2 | Maintain shared definitions (thresholds, segments) | MVP | Supp | - | Data, Gov | Owner of definitions |
| F-61 | 5.2 | Manage AI skills, prompts and templates | MVP | Supp | - | AI | Change control |
| F-62 | 5.3 | Run routines on schedule, no manual effort | MVP | RFP | Ops | - | - |
| F-63 | 5.3 | Alert on failed or incomplete runs | MVP | Supp | Ops | - | Who responds |
| F-64 | 5.3 | Recover and retry failed runs | MVP | Supp | Ops | - | Recovery expectations |
| F-65 | 5.3 | Monitor consumption and cost | MVP | Supp | Ops | - | Budget limits |
| F-66 | 5.3 | Record audit trail | MVP | Supp | - | - | Required audit records |
| F-67 | 5.3 | Provide operating handover to a NAVEX engineer | MVP | RFP | Ops | - | Named engineer |
| F-68 | 5.4 | Agree acceptance criteria | MVP | Supp | Gov | - | Criteria and sign-off owner |
| F-69 | 5.4 | Evaluate output quality | MVP | Supp | - | - | Test method and set |
| F-70 | 5.4 | Define success metrics and baselines | MVP | NAVEX | Gov | - | Which metrics |
| F-71 | 5.4 | Track usage and adoption | MVP | RFP | App | - | - |

Evidence that drives several gaps (Gap matrix, column "What exists today"):
- Scoring runs weekly in Claude skills through the Enterpret MCP connector. About 80-90% of it is reproduced in Snowflake and Power BI.
- Most at-risk accounts showed "taxonomy data pending". Narratives existed only for a minority of at-risk accounts, all Red.
- An internal test rated Enterpret about 90% and Snowflake Gen AI about 50% on output quality. The method was not documented.
- Ownership data is incomplete: some at-risk accounts have no CXM, most lack an exec sponsor, and the manager filter is "coming soon".
- Definitions differ between documents: in-scope ARR is $100K+ in the guide and $50K+ in the report, and there are 13 or 14 domains. Rules AY2 and AY4 never appeared in the report.
- Informal baseline: about 3 business days from feedback to teams. No programme metrics exist.

## Use cases (Gap xlsx, Use Cases)

| UC | User | Use case | Phase | Basis |
|---|---|---|---|---|
| UC-01 | CXM | Review own accounts, understand friction, inspect evidence, record action (scope TBC) | MVP | Partly inferred |
| UC-02 | CXM manager / director | Find priority accounts; investigate team friction; escalate | MVP, scope TBC | Partly inferred |
| UC-03 | Product manager | Domain friction, on-demand research, Fact Base briefings | P1; Fact Base TS | Partly inferred |
| UC-04 | Product leadership | Compare issues across domains for the Product Business Review | P1 | Partly inferred |
| UC-05 | AE / sales | Prepare account conversations | P1, needs scoping | To define |
| UC-06 | ELT / CXO | Agreed executive customer-intelligence brief | P1 | Partly inferred |
| UC-07 | Marketing / Product Marketing | Customer language, needs, competitive themes | P1 broader, to validate | To define |
| UC-08 | Finance / RevOps / other | To define | P1, scope TBC | To define |
| UC-09 | VoC analysts (CSOps / ProdOps) | Manage outputs, maintain skills, curate knowledge, fix exceptions | MVP onward | Stated / inferred |
| UC-10 | VoC programme owner | Roadmap, acceptance, success measurement | MVP onward | Stated (RFP) |
| UC-11 | Scoring model owner | Approve scoring rule changes | MVP onward | Stated (call) |
| UC-12 | NAVEX platform engineer | Monitor runs, fix failures, deploy changes | MVP onward | Stated (RFP) |
| UC-13 | Data / integration owners | Source readiness, mappings, refreshes, output contracts | MVP onward | Stated (call) |
| UC-14 | Security / identity / legal | Approve access, processing, evidence-disclosure controls | MVP onward | Stated (RFP) |
| UC-15 | Downstream system users | See scores and narratives in Gainsight, Salesforce, Power BI | MVP (Power BI TBC) | Stated |

## Top effort decisions and risks (Gap xlsx, Decisions & risks)

| # | Type | Item | Lower-effort case | Higher-effort case |
|---|---|---|---|---|
| 1 | Decision | Where AI runs: Snowflake Cortex only, or Claude directly | Claude via Cortex approved | Two AI platforms approved separately |
| 2 | Risk | Scoring moves from skills to exact rules while models change (call transcripts) | Snowflake version close; small dated changes | Large nuances or late changes |
| 3 | Risk | Ownership data incomplete for role-based access | Clean master system | Clean-up and governance first |
| 4 | Decision | Knowledge hub location (not Snowflake or Enterpret) | Small curated set on an existing approved platform | New platform plus security review |
| 5 | Decision | Where CXMs work; churn, action recording, escalations | Gainsight via the existing data share | New app plus action, escalation, churn views |

Also open: the Enterpret access method (F-38). Missing success metrics (F-70) affect how value is shown, not effort.

## Candidate solution paths (Gap xlsx, Solution Approach)

Common to every path: Snowflake as hub, Enterpret reused, per-source access via Snowflake, API or MCP; daily scoring with coverage and reconciliation checks; scheduled, evidence-backed explanations; Snowflake write-back with history; downstream systems read from Snowflake; governed knowledge hub outside ingestion; enterprise sign-on plus role and account restriction; handover to a NAVEX engineer.

| | Path 1 Streamlit | Path 2 Custom app, Snowflake-led services | Path 3 Custom app, dedicated orchestration |
|---|---|---|---|
| Processing | Snowflake-led | Snowflake-led | Separately hosted backend using approved AI services |
| Choose when | Streamlit meets user needs | Usability, concurrency or integration need it; Snowflake services suffice | Processing needs more control than Snowflake-led allows |
| Trade-off | Less UX control | More app development and maintenance | More infrastructure; hosting and AI boundary approval |

The Proposal later recommended a React app with a Snowflake and Cortex backend, which is closest to Path 2 (Proposal slide 3).

## Conflicts with docs/

| Topic | Workbook | docs/ |
|---|---|---|
| Solution path | Paths 1 to 3 open; the Proposal recommends a Snowflake-led backend | Path 3 shape: AWS backend, agent on Amazon Bedrock AgentCore (`docs/02-architecture/overview.md`) |
| AI boundary | Data lead stated "self-contained in Snowflake using Cortex, no LLM outside" (F-58) | Model calls run outside Snowflake, on AgentCore (same file) |
| Rule codes | AY2 and AY4 never appeared in the report (F-03) | AY2 "Yellow repeat" listed; no AY4; AR4 is churn language (`requirements.md` ACC-04, Confirm) |
| In-scope ARR threshold | $50K+ (report) vs $100K+ (guide), unresolved (F-60) | ARR tier fixed at $50K (`requirements.md` ACC-06; `glossary.md` "ARR tier") |
| Snowflake write-back, Gainsight and Salesforce feeds | MVP, explicit in the RFP (F-50 to F-52) | Snowflake read only; Gainsight link only in the MVP (`overview.md` "Data sources") |
| Record action taken | TBC (F-19) | Removed; CXMs log in Salesforce and Gainsight (`requirements.md` "Removed from the MVP") |

## Open questions

- The workbook cites "AI platform (F-55)" for F-06 and F-28, but F-55 is ownership mapping; the AI boundary is F-58. Its "rule changes assessed in F-56" means F-59. Corrected above; not confirmed with the author.
- Business criticality per function is blank; NAVEX is to set it (Feature List sheet).
