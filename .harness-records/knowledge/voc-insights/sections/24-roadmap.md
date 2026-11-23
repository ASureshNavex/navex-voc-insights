# Roadmap

Sources: `NAVEX_VoC_Platform_Solution_Roadmap_Diagram_V3.png` (Roadmap png, Oct 2026); `NAVEX VoC - Technical Architecture and Sizing.pptx` (Arch deck slides 2, 9-10, 16); `NAVEX_VoC_Cost_and_Infrastructure_by_Environment.xlsx` (Cost xlsx, Inventory "Required from", Checklist rows 19-20); `navex-voc-platform-scaffold.zip` (unit list U01-U22).

## Already in docs/ (read there, not here)

- Phase dates and one-line scope: `docs/01-product/overview.md` "Phases" (MVP 26 Oct - 8 Dec 2026; Phase 1 9 Dec 2026 - 15 Feb 2027; Phase 2 16 Feb - 30 Mar 2027). Matches Arch deck slide 2.
- MVP definition of done: `overview.md` "MVP definition of done"; `docs/02-architecture/hld.md` section 1.
- MVP build order (waves 1-4): `docs/04-delivery/units-of-work.md` "Suggested order".

## Milestones

| Milestone | Phase | Window | Theme (Arch deck slide 2) |
|---|---|---|---|
| M1 | MVP | to 8 Dec 2026 | VoC Insights Workspace for CXM, CXM leadership, AE, ELT, VoC admin; Refresh Agent (productionised RYGG skills); change-of-status alerts and digests; Knowledge Hub upload and approval |
| M2 | Phase 1 | 9 Dec 2026 - 15 Feb 2027 | Product workspace and Product Domain Friction Report; deep dives for red and yellow domains; Insights agent with cited answers; approved Knowledge Hub files as evidence |
| M3 | Phase 2 | 16 Feb - 30 Mar 2027 | Four-quadrant Fact Base by product domain; Living and Initiative Fact Base linked to Aha!; competitive intelligence from Klue; Executive, Finance and Sales views |

## By tier (Roadmap png)

| Tier | Current state (manual, two people) | MVP (M1) | Phase 1 (M2) | Phase 2 (M3) |
|---|---|---|---|---|
| 1 Consumers | CXM weekly HTML; Product monthly domain report; ELT/AE on request | CXM and leadership: daily view, own book | Product and leaders (self-serve domain view); AEs and ELT (scoped accounts, curated reports) | Business teams: Marketing, Finance, RevOps, Sales |
| 2 Experience | Static HTML on SharePoint; Power BI | React web app; Power BI embedded | Claude assistants in the same app; curated report library (QBR briefs, ELT, business reports) | On-demand briefings (Fact Base to Product) |
| 3 Identity | No role-based access | OIDC SSO, group sync, RBAC: role, book, region | Entitlements extended to Product, AE, ELT, business | No change |
| 4 Interface | No API; skills call systems | Experience API, user token every call | MCP gateway wrapping API capabilities | Further MCP sources on the same gateway |
| 5 Capabilities | Claude projects and skills; churn model (XGBoost in Snowflake) | Scoring, Narrative, Evaluation (benchmark gates each release), Run control | Insights agent; Report service; Domain scoring | Fact Base agent |
| 6 Ports | SQL and MCP calls inline | Feedback data, Classification, AI inference, Knowledge, Distribution | Live data (Klue, Pendo over MCP) | Classification repointed to in-platform classifier |
| 7 Data platform | Snowflake, Enterpret | Snowflake, Enterpret (at measured parity), knowledge store | Canonical entities, VoC taxonomy (NAVEX-owned, versioned), knowledge graph | In-platform classification; alternative platform via adapters |
| 8 Sources and downstream | Five feedback sources; exec sponsor in a spreadsheet; CAB notes not captured | Ingestion and distribution services; write-back to CRM, Power BI | Market data: Klue, Pendo usage | Further sources via same ports |

Cross-cutting by phase (Roadmap png): Security (current), Operations (MVP: scheduled runs, alerts, retry, cost monitoring), Model governance (P1: versioned rules, prompts, skills, taxonomy), Evidence and quality (P2: expert benchmark, traceable evidence).

## Infrastructure by phase (Arch deck slides 9-10, 16; Cost xlsx)

| Phase | Adds |
|---|---|
| MVP | Full network, edge and data path; Refresh Agent on AgentCore Runtime with AgentCore Identity and Observability |
| Phase 1 | Insights agent (Runtime), AgentCore Gateway, Identity federated with Entra, Memory; Bedrock Knowledge Bases on S3 Vectors; monthly product-domain run in the Refresh Agent; Product roles in Entra |
| Phase 2 | Fact Base agent; NAT egress and Fargate connector tasks for Klue, Pendo, Aha!; provisioned Bedrock throughput when volume is steady |

## Scaffold unit plan (scaffold, older)

| Phase | Units |
|---|---|
| MVP | U01 platform-foundation, U02 identity-entitlement, U03 capability-ports, U04 feedback-data-adapter, U05 classification-adapter, U06 inference-adapter, U07 knowledge-service, U08 scoring-service, U09 narrative-service, U10 evaluation-service, U11 run-control, U12 ingestion-service, U13 distribution-service, U14 experience-api, U15 web-app |
| Phase 1 | U16 mcp-gateway, U17 insights-agent, U18 report-service, U19 domain-scoring, U20 business-ontology |
| Phase 2 | U21 fact-base-agent, U22 in-platform-classification |

The skeleton replaced this with FND/API/WEB/ING/AGT/NTF/OPS units (`units-of-work.md`).

## Conflicts with docs/

| # | Topic | Sources | docs/ |
|---|---|---|---|
| 1 | Phase 1 content | Arch deck slide 2 lists no Gainsight write-back for Phase 1 | `overview.md` "Phases" lists Gainsight write-back in Phase 1; `lld.md` 4.5 agrees |
| 2 | Knowledge Hub phase | Arch deck slide 2: upload and approval in MVP | `hld.md` 12 item 11 and `lld.md` 9: phase still to confirm (scope workbook says late Phase 1) |
| 3 | Power BI and Evaluation in MVP | Roadmap png (Oct): Power BI embedded and Evaluation service in M1 | Neither appears in `overview.md` components or `units-of-work.md`; Arch deck slide 4 (Nov) also omits them |

## Open questions

- Is Evaluation (benchmark release gate) an MVP deliverable or dropped?
- Is Power BI embedding still planned, and in which phase?
- Does the business ontology (entities, taxonomy, knowledge graph) remain Phase 1 work? It is absent from the Arch deck inventory.
