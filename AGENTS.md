# NAVEX VoC Insights Workspace: guide for AI coding agents

This file orients any AI harness (Claude Code, GitHub Copilot, Cursor, Codex, AWS AI-DLC tooling) and any new developer. `CLAUDE.md` points here.

## What this is

NAVEX's internal view of customer friction by account. It rebuilds the At-Risk Account Scorecard as a platform that refreshes on a schedule, alerts account owners when a status changes, and is reached through NAVEX SSO. MVP go-live is 8 December 2026. Read `docs/01-product/overview.md` first.

## Where things are

| Need | Go to |
|---|---|
| What to build, with acceptance checks | `docs/01-product/requirements.md` |
| What to work on next | `docs/04-delivery/units-of-work.md` |
| Who can see and do what | `docs/01-product/roles-and-access.md` |
| Unanswered questions and the assumption in the code | `docs/01-product/open-items.md` |
| How the system fits together | `docs/02-architecture/overview.md`, `decisions.md`, `lld.md` |
| Screen content, labels and layout | `docs/reference/prototype/voc-insights-workspace-latest.html` |
| Endpoint list and build status | `docs/03-engineering/api-contract.md` |
| Setup and commands | `docs/03-engineering/local-setup.md` |
| Sign-in and AWS access | `docs/03-engineering/sso-and-aws-access.md` |
| Source-level detail behind the docs: exact scoring rules, decisions, conflicts | `.harness-records/knowledge/voc-insights/SPEC.md`, then one section |

| Code | Path | Skill to load first |
|---|---|---|
| React web app | `apps/web` | `navex-voc-frontend-architecture`, `react-tailwind-shadcn-scss-dashboard` |
| FastAPI Experience API | `services/experience-api` | `navex-fastapi-rest-apis` |
| Account Scoring Agent, LangGraph on AgentCore | `services/account-scoring-agent` | `navex-agentcore-runtime` |
| Ingestion task | `services/ingestion` | `navex-fastapi-rest-apis` for Python conventions |
| Notification task | `services/notifications` | `navex-fastapi-rest-apis` for Python conventions |
| Tables and migrations | `packages/voc-data` | |

Each skill has one body in `.harness-records/skills/<name>/SKILL.md`, with its reference files beside it; `.claude/skills/<name>/SKILL.md` is only a pointer that lets Claude Code find it, so a skill is changed in the body, never the pointer. `clean-lean-architecture-code` applies to every file. Run `navex-security-code-review` on every change before calling it done.

## How to work

Any change that designs or alters behaviour, a unit from `units-of-work.md`
included, goes through `/sgivp`: Search (knowledge base, then `docs/`, then
the code, then the web), Ground (against the rules, decision records,
requirements and open items), options for a person to choose, a plan for a
person to confirm, then implement with tests first, verify, and prune. Follow
the existing pattern: `domains/accounts` for an API domain,
`features/accounts` for a web feature, `graphs/account_scoring` for agent work.

| Workflow skill | Use for |
| --- | --- |
| `sgivp` | Every design or behaviour change, started by a person |
| `test-design` | Module-level and functionality-level tests, and which requirement checks have one |
| `open-item-settlement` | An answer to an open item, or a conflict between `docs/` and the knowledge base |
| `bug-fix` | A defect: reproduce it as a failing test, fix the cause, verify, prune |
| `pr-ready` | Before a pull request: impact, the tests that prove it, security review, the PR body |
| `release-check` | Go-live or phase readiness, each check pass, fail or unknown |
| `knowledge-refresh` | New NAVEX documents into `.harness-records/knowledge/voc-insights/` |
| `session-handoff` | Close a task in `CONTEXT.md`; open one from it |

## Rules that are never broken

`.harness/CONSTITUTION.md` lists them: the Navex core (N1 to N10), then this
repository's own rules, P1 to P13, which are changed in
`.harness/project-constitution.md`. Read the list once per session and cite a
rule by its id.

## Commands

```bash
# Python, from the repository root
uv sync --all-packages
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest

# Web, from apps/web
npm install
npm run typecheck && npm run lint && npm test && npm run build

# Database
docker compose up -d postgres
cd packages/voc-data && uv run alembic upgrade head
```

## When something is unclear

Check `open-items.md`. If the question is there, build to the stated assumption and keep it in one place. If it is not, stop and ask rather than guess; add the question to `open-items.md`.
