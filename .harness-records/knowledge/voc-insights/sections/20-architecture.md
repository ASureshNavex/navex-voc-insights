# Logical architecture

Sources: `NAVEX VoC - Technical Architecture and Sizing.pptx` (Arch deck, 17 Nov 2026, slides 2-14); `NAVEX_VoC_Platform_Architecture_Diagram.png` (Platform diagram, Oct 2026); `NAVEX_VoC_AWS_MVP.drawio`, `NAVEX_VoC_AWS_Target.drawio` (drawio, 4 Nov 2026; edges carry labels only, no source or target ids); `navex-voc-platform-scaffold.zip` (`STRUCTURE.md`).

## Already in docs/ (read there, not here)

- Components, runtime, tech, code path per unit: `docs/02-architecture/overview.md` "Components".
- Request flow and refresh flow (ingestion task, then Account Scoring Agent): `overview.md` "How a request flows", "How a refresh flows".
- Settled decisions 1-15: `docs/02-architecture/decisions.md`. HLD ADR-01..08: `docs/02-architecture/hld.md` section 10.
- Context, external systems and protocols: `hld.md` section 4. Building blocks: `hld.md` section 6.
- Refresh stages, notification jobs, failure behaviour: `docs/02-architecture/lld.md` 2.3.
- Knowledge Hub upload and approval state machine: `lld.md` 2.4 and 5.6.
- Enterpret calls, Snowflake access, email format, Gainsight link: `lld.md` 4.2-4.5.
- Deployable units, events, IAM per unit: `infra/README.md`.

## What the sources add

### Layered model (Platform diagram; Arch deck slides 3-4)

| Layer | MVP (slide 4) | Phase 1 adds | Phase 2 adds |
|---|---|---|---|
| Consumers | CXM, CXM leadership, Account executives, ELT, VoC admin ("five roles, each with its own data scope") | Product, Product leadership | Business teams (seven roles total, slide 3) |
| Experience | React web app: one view of accounts, themes, verbatim; Knowledge Hub; digest preferences; admin. "One front door" | "Claude assistants": agent path for research and briefings, cited answers ("two front doors") | |
| Interface | Experience API: versioned REST, validates token, binds scope into every query | MCP gateway: tools wrap the same API capabilities under identical RBAC | Further MCP sources on the same gateway (Roadmap png) |
| Capability services | Refresh Agent, Scoring rules (AR1-AR4, AY1-AY3 in code), Summary service, Notification task, Knowledge Hub, Saved views and export, Run control (publish, retry, last good run), Usage and audit | Insights agent, Report service, Domain scoring (Product friction report) | Fact Base agent |
| Integration ports | Feedback data (Snowflake SQL and views), Classification (Enterpret MCP API), AI inference (Amazon Bedrock), Knowledge (S3 document store), Distribution (email and deep links) | Live data (MCP: Klue, Pendo) | Classification repointed to an in-platform classifier |
| Data platform | Snowflake (account master, ARR, renewal, owners, churn score), Enterpret (classification; taxonomy owned by NAVEX), Knowledge Hub store, PostgreSQL serving store | Business ontology: canonical entities, VoC taxonomy, knowledge graph | Alternative data platform, adopted by swapping adapters only |
| Downstream | Gainsight (CTA and deep link), Salesforce (account record link), Email (alerts, digests) | | Power BI appears in the Oct diagram and drawio only |

Rule stated on every diagram: services call ports, never a vendor directly; adapters are SQL, MCP API, object store (slide 4; scaffold `STRUCTURE.md` "Port catalogue").

### Refresh Agent graph as the deck draws it (slides 11-12)

One LangGraph graph on AgentCore Runtime, started by EventBridge Scheduler 3 times a day. Numbered flow:

| Order | Step | Kind | Pydantic output | PostgreSQL target |
|---|---|---|---|---|
| 1 | Scheduler triggers run (edge 1) | | | |
| 2 | Scoring queries (edge 2) to Enterpret MCP, 4 batches | Deterministic | AccountSignal | account_signal |
| 3 | Rule engine AR1-AR4, AY1-AY3; scoring model version stored with run | Deterministic | AccountRating | account_rating |
| 4 | Taxonomy (L1-L3 themes with volumes) and verbatim pulls (source, date, citation) | Deterministic | ThemeCount, Verbatim | account_theme, account_verbatim |
| 5 | Red issue review: Enterpret Issues query, label open, closed or none | Deterministic | IssueStatus | account_rating |
| 6 | Summaries: Jinja2 template, Bedrock invoke (edge 7) structured output | Prompt | AccountSummary | account_rating |
| 7 | Validate Pydantic models | Deterministic | RunResult | refresh_run |
| 8 | Enrich and persist (typed JSON, edge 9; Snowflake, edge 10): Snowflake ARR, renewal, NPS, owners, exec sponsor joined in code; KPIs as SQL views | Deterministic | AccountProfile | account, kpi views |
| 9 | Insert, publish run (edge 11) | | | |
| 10 | EventBridge rule (edges 12-13) `run.published` starts Notification task (alerts) | | StatusChange | status_change_event |

- Week-over-week: SQL comparison against the previous confirmed status (slide 12, "Phase 8").
- HTML render of the manual skills is retired; workspace reads PostgreSQL (slide 12). Decided.
- Enterpret volume per run: 21 graph queries (4 scoring, 8 taxonomy, 8 verbatim, 1 Issues) (slide 18).

### Experience API flow (slide 13)

HTTPS -> CloudFront/WAF (S3 static site via OAC) -> load balancer `/api` -> Experience API (scope, friction report, export) -> verify token against Entra signing keys (cached) -> read PostgreSQL by scoped ids -> drill-down to Snowflake over PrivateLink for record-level evidence. Phase 1: AgentCore Gateway (MCP tools with user scope) delegates to Insights agent, which grounds on Knowledge Bases (approved files).

### LLM use

| Use | Phase | Where |
|---|---|---|
| Account summaries (explanation of rating) | MVP | Refresh Agent node, Bedrock, Pydantic structured output |
| Account briefs | MVP | Bedrock on request (slide 15: 300 a month MVP) |
| Topic research, cited answers | Phase 1 | Insights agent + Bedrock Knowledge Bases |
| Fact Base narratives | Phase 2 | Fact Base agent |

Scoring is never a model (slide 12, all scoring steps "Deterministic").

### Scaffold port catalogue (older target design, scaffold `STRUCTURE.md`)

Seven ports: FeedbackDataPort, ClassificationPort, InferencePort, KnowledgePort, DistributionPort, LiveDataPort, EntitlementPort; each with one contract, adapters, and a test fake. Swap candidates named: Databricks, Fabric, Postgres (feedback); in-platform classifier; platform-hosted models; SharePoint, Confluence (knowledge); reverse ETL (distribution).

## Conflicts with docs/

| # | Topic | Sources say | docs/ says |
|---|---|---|---|
| 1 | Background unit split | One "Refresh Agent" on AgentCore does pull, score, summarise, publish (Arch deck slides 10-12); drawio shows "Run control worker, Fargate Spot" | Ingestion task on ECS Fargate then Account Scoring Agent on AgentCore (`overview.md` "How a refresh flows"; `decisions.md` 3a). docs flags the diagrams as predating the split **Resolved 2026-11-19: split, scoring is the Account Scoring Agent (adr/0004).** |
| 2 | Graph nodes | Scoring queries, rule engine, taxonomy/verbatim, red issue review, summaries, validate, then enrich/persist (slide 11) | `load_batch`, `score`, `summarise`, `publish`; pulls happen in ingestion (`overview.md`) |
| 3 | When Snowflake is read | After the graph, "Enrich and persist" joins ARR, owners etc. (slide 11 step 10) | Ingestion pulls accounts from Snowflake first and matches feedback to them (`overview.md`; `lld.md` 2.3 stages 2 and 5) |
| 4 | Notification image | Notification task is "Same image, Fargate" (slide 7 label); HLD 6 also says same image | Separate `services/notifications/Dockerfile` (`infra/README.md` "Deployable units") |
| 5 | Where RBAC is enforced | "Enforcement at the source: row and column security applied in the data platform" (slides 3-4, Platform diagram) | Scope bound into the PostgreSQL query by the API (`decisions.md` 7; `hld.md` ADR-02); slide 13 text agrees with docs |
| 6 | Refresh schedule | drawio: EventBridge Scheduler "Daily 02:00" | Three runs a day (`hld.md` 6, `lld.md` 2.3); Arch deck slide 11 agrees with docs |
| 7 | Downstream Power BI | Oct diagram and drawio list Power BI downstream; Roadmap png has Power BI embedded in MVP | Not in `hld.md` 4 context; deck slide 4 MVP drops it |

Source-to-source: AI inference port is "Claude, approved boundary" in the Oct diagram and scaffold, "Amazon Bedrock" in the Nov deck; Classification is "Enterpret REST API" in the Oct diagram and scaffold, "Enterpret MCP API" in the deck. The Nov deck is the latest.

## Open questions

- Is the Evaluation service ("expert benchmark gates each release", Platform diagram; scaffold U10) still in MVP scope? Absent from deck slide 4 MVP.
- Is Power BI embedding (Roadmap png, MVP M1) in or out?
- Does the business ontology (canonical entities, taxonomy, knowledge graph) land in Phase 1 as drawn? Not in the deck inventory.
