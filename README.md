# NAVEX VoC Insights Workspace

The At-Risk Account Scorecard rebuilt as a platform: a Red, Yellow or Green VoC rating for every account with the themes and customer words behind it, refreshed on a schedule, with change-of-status alerts and access through NAVEX SSO.

MVP go-live: 8 December 2026.

## Start here

| You want to | Read |
|---|---|
| Understand the product | `docs/01-product/overview.md` |
| See what must be built | `docs/01-product/requirements.md` |
| Pick up work | `docs/04-delivery/units-of-work.md` |
| Set up your machine | `docs/03-engineering/local-setup.md` |
| Configure sign-in and AWS access | `docs/03-engineering/sso-and-aws-access.md` |
| Use an AI harness | `AGENTS.md` and `.claude/skills/` |

## Layout

```text
apps/web/                        React 19 single page application
services/experience-api/         FastAPI REST API, /api/v1
services/ingestion/              Pulls, matches, masks and stages source data (ECS task)
services/account-scoring-agent/  Scores, explains and publishes (LangGraph on AgentCore Runtime)
services/notifications/          Change-of-status alerts and digests (ECS task)
packages/voc-data/               Tables, scope filter, migrations
docs/                            Knowledge base: product, architecture, engineering, delivery, reference
.claude/skills/                  Seven engineering skills
infra/                           Contract between the code and the NAVEX-provisioned environments
```

## Quick check

```bash
uv sync --all-packages && uv run ruff check . && uv run mypy && uv run pytest
cd apps/web && npm install && npm run typecheck && npm run lint && npm test && npm run build
```

Both run with no NAVEX access.

## What the skeleton contains

| Area | In place | Next |
|---|---|---|
| Web | Corp AD sign-in, entitlements, permission guards, app shell with bell icon, theme, loaders, scorecard reference slice | Remaining scorecard parts and the other screens, each a placeholder naming its unit |
| API | Token verification, role and scope resolution, paging, errors, audit; accounts, portfolio summary and saved views built; all 41 operations published in the contract | The 33 contract-only operations |
| Ingestion | Pipeline, masking, matching, staging, hand-over to the agent | Snowflake and Enterpret field mapping |
| Scoring agent | LangGraph graph, rule set interface, triggers, theme ranking, status confirmation, summary prompt, atomic publish | NAVEX rule set, AgentCore deployment |
| Notifications | Idempotent change-of-status alerts | Digests |
| Data | 20 tables, scope filter, baseline migration checked on PostgreSQL 16 | Seed data |

Open decisions with NAVEX are in `docs/01-product/open-items.md`.
