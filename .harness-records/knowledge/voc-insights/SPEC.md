# VoC Insights knowledge index

Distilled from the engagement material (FRD, discovery closure, solution
proposal, architecture deck, domain and RYGG models, scoring skills, cost and
scope workbooks, meeting notes and transcript, workspace mockups), built
2026-11-19. The source documents are not in this repository.

## How to read this

- `docs/` is the product's own documentation and wins for what to build:
  requirements, roles, architecture, API contract, units of work. Start there
  (`AGENTS.md`, "Where things are").
- This folder holds what `docs/` does not: the reasoning, the exact scoring
  rules, the source-level detail, and every place the sources and `docs/`
  disagree. Each section points to `docs/` instead of restating it.
- Read this index, then only the one section a task needs. Every fact cites
  its source document; "Decided", "Assumed" and "Open" mark its standing.
- A conflict marked **Resolved** points to a record under `adr/`. An
  unresolved one is an open question: follow `docs/` and raise it, never
  pick a side silently.

## Sections

| File | Holds |
| --- | --- |
| `sections/01-product-overview.md` | Discovery context: decisions by Customer Success and Product, the as-is capability chain, systems `docs/` omits, root causes, validation and value |
| `sections/02-functional-requirements.md` | 16 FRD requirements with no row in `docs/01-product/requirements.md`, FRD dependencies mapped to open items, 14 conflicts |
| `sections/03-scope-phase-1-and-target.md` | Milestone plan, phase view, function counts, phase-placement disagreements |
| `sections/04-feature-gap-assessment.md` | Features F-01 to F-71, use cases UC-01 to UC-15, gaps and solution paths |
| `sections/10-domain-model.md` | Feedback sources, Enterpret graph entities, account and record fields, product domains |
| `sections/10a-product-domain-scoring.md` | Domain RYGG: tiers, P75 / P90 thresholds, volume floor, breadth rule, trend flag |
| `sections/11-rygg-account-scoring.md` | Account rules AR1-AR4, AY1-AY4 with exact thresholds, churn filter, segment cohorts, sort, week over week |
| `sections/12-friction-scoring-pipeline.md` | The scoring skills step by step (1a-1d, 2, 3), their JSON schemas and hand-offs |
| `sections/13-report-outputs.md` | At-Risk, Domains and detail report layouts |
| `sections/13a-fact-base-outputs.md` | Fact Base slide and HTML, topic brief, account product brief |
| `sections/20-architecture.md` | Layers by phase, the deck's agent graph, API flow, where an LLM is used |
| `sections/21-aws-infrastructure-and-environments.md` | AWS inventory per environment, network paths, what each phase adds |
| `sections/22-cost-and-sizing.md` | Sizing basis and the cost models |
| `sections/23-identity-and-sso.md` | Entra per environment, roles by phase, machine and agent identities |
| `sections/24-roadmap.md` | Milestones M1-M3 by tier and infrastructure, scaffold units U01-U22 |
| `sections/25-codebase-layout.md` | The scaffold compared with this repository's layout |
| `sections/30-decisions-log.md` | Dated decisions from the notes and transcript, later wins |
| `sections/31-workspace-ux.md` | Mockup versions compared: screens, navigation per role, filters, states |
| `sections/32-ui-feedback.md` | Feedback items with done / open status |
| `sections/33-react-handover.md` | Handover component names mapped to this repository, expected data types, contract conflicts |
| `sections/34-open-questions-and-risks.md` | Open questions not in `docs/01-product/open-items.md`, risks, assumptions |
| `sections/40-glossary-additions.md` | Terms `docs/01-product/glossary.md` does not define |

## Decisions settled since the sources

| Record | Decision |
| --- | --- |
| `adr/0001-environments-are-dev-qa-staging-prod.md` | Environments are DEV, QA, Staging, Prod |
| `adr/0002-the-workload-region-is-us-west-2.md` | The workload region is us-west-2 |
| `adr/0003-the-cost-baseline-is-311-to-469-usd-a-month.md` | Cost baseline 311 USD a month (MVP) to 469 (Phase 1 and 2) |
| `adr/0004-scoring-is-its-own-agent-split-from-the-refresh-agent.md` | Scoring is the Account Scoring Agent; ingestion is its own task |

## The conflicts that matter most, still open

- Rating model: the sources have rules and four ratings with no numeric
  score; `docs/` assumes a 0-100 friction score and three ratings, and its
  ACC-04 rule codes mean something different (sections/11).
- Account join key: the skills join on account name; `docs/` on Salesforce ID
  (sections/11).
- AI runtime and Snowflake: the proposal recommends Snowflake Cortex and
  write-back in the MVP; `docs/` runs on Bedrock AgentCore with Snowflake read
  only (sections/02, 20).
- Contract details between the mockup handover and `docs/`: identity
  endpoint, `/api/v1` prefix, casing, money type (sections/33).
