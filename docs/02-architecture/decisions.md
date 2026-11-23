# Architecture decisions

One entry per decision that shapes the code. Add a new entry when a decision changes; do not rewrite history.

| # | Decision | Reason | Consequence |
|---|---|---|---|
| 1 | One repository for the web app, four services and the shared data package | A small team, one release train, shared contracts | Python uses a `uv` workspace with one lockfile; the web app has its own `package.json` |
| 2 | Tables and migrations live in `packages/voc-data`, not inside the API service | The API, the ingestion task, the agent and the notification task all use the same tables | The FastAPI skill shows `alembic/` in the service; here it sits in the shared package and each service depends on it |
| 3 | Scoring runs as the Account Scoring Agent, a LangGraph graph on AgentCore Runtime | NAVEX's standard for agents | Runtime entry point in `entrypoint.py`; Gateway, Identity and Memory arrive in Phase 1 |
| 3a | The deterministic steps before scoring run outside the agent, as the ingestion task on ECS Fargate | Pulling, matching and masking need no reasoning; an ordinary task is cheaper, simpler to retry and easier to test | Two units and one hand-over: the task stages evidence per run and starts the agent with the run ID |
| 4 | Scoring is code; only summaries use a model | Ratings must be reproducible and cheap | The agent graph has a fixed order; the model never chooses a step or a tool in the MVP |
| 5 | Prompts are Jinja2 files rendered with `StrictUndefined` from typed context models | Reviewable prompts that fail fast on a missing variable | `tests/test_prompts.py` renders every template |
| 6 | The API reads only the published run | A failed refresh never removes good data | Every read joins through `published_run` |
| 7 | Role and data scope are separate | The same role can have different reach, for example Sales and Sales leadership | Entitlements carry both; queries use scope, screens use permissions |
| 8 | Access tokens stay in memory | Tokens in browser storage are readable by injected script | MSAL cache is `memoryStorage`; a page reload signs in silently through the Entra session |
| 9 | A typed `fetch` wrapper is the single HTTP client | One place for the bearer token and `401`/`403` handling, with no extra dependency | Components never call `fetch` directly |
| 10 | UI primitives are native HTML elements styled with the shadcn/ui recipes and Tailwind | Accessible by default, familiar to every React developer, nothing bespoke to maintain | `button`, `input` and `select` are real elements; no custom dropdown widgets |
| 11 | Theme values are SCSS variables mapped to shadcn CSS variables | One edit rebrands the app | Colours never appear as hex values in components |
| 12 | Tailwind runs through PostCSS so SCSS partials can use `@apply` | Tailwind's Vite plugin handles only `.css` files | `postcss.config.js` loads `@tailwindcss/postcss` |
| 13 | Tests run on SQLite in memory; migrations target PostgreSQL | Fast tests with no container | Models avoid PostgreSQL-only column types; JSON columns use the JSONB variant on PostgreSQL |
| 14 | Local development uses AWS CLI v2 named profiles on the `navexsso` session | NAVEX replaced IAM users with Corp AD federation | No static AWS keys anywhere; see `03-engineering/sso-and-aws-access.md` |
| 15 | Top bar with tabs, notifications behind a bell icon | Matches the latest prototype and NAVEX's direction | Only `AppShell.tsx` knows the navigation pattern |
