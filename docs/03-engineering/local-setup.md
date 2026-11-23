# Local setup

## Tools

| Tool | Version | Used for |
|---|---|---|
| Git | Current | Source control |
| Python | 3.13 | Services |
| uv | Current | Python dependencies and virtual environment |
| Node.js | 22 LTS | Web app |
| Docker Desktop | Current | Local PostgreSQL, image builds |
| AWS CLI | v2 | AWS access through NAVEX SSO |
| VS Code | Current | Editor; accept the recommended extensions when prompted |

## First run

```bash
# 1. Python workspace: one virtual environment for all four services
uv sync --all-packages

# 2. Database
docker compose up -d postgres
cd packages/voc-data && uv run alembic upgrade head && cd ../..

# 3. Check everything
uv run ruff check . && uv run mypy && uv run pytest

# 4. Web app
cd apps/web
npm install
npm run typecheck && npm run lint && npm test
```

These steps need no NAVEX access. Tests run on in-memory SQLite and on fakes for Snowflake, Enterpret, Bedrock and email.

## Running the app locally

Signing in needs the Entra app registrations from NAVEX IT. Until those exist, work test-first.

```bash
# API, from services/experience-api
cp .env.example .env        # set ENTRA_TENANT_ID and ENTRA_API_AUDIENCE
uv run uvicorn app.main:app --reload --port 8000

# Web, from apps/web
cp .env.example .env        # set the three VITE_ENTRA and VITE_API values
npm run dev                 # http://localhost:5173
```

The web dev server proxies `/api` to the API, so the browser sees one origin, as it does behind CloudFront.

The same commands are VS Code tasks: Terminal, Run Task, then "Database: start", "API: run", "Web: run", "Quality gate: Python" or "Quality gate: Web".

For anything that touches AWS (S3, Bedrock, Secrets Manager), sign in first: `aws sso login --profile navexdev`. See `sso-and-aws-access.md`.

## What needs NAVEX before it runs

| To run | You need |
|---|---|
| Sign-in in the browser | SPA and API app registrations; your account in a mapped Corp AD group |
| Ingestion against real sources | Snowflake service user and key, the account view name, the Enterpret MCP URL and token in Secrets Manager |
| Summaries | Bedrock model access in the DEV account and the model ID |
| Alert emails | A verified sender for `voc-insights@navex.com` |

## Working on a requirement

1. Pick a unit from `docs/04-delivery/units-of-work.md`.
2. Read its requirements in `docs/01-product/requirements.md` and open the prototype for the screen.
3. Read the skill for the area in `.harness-records/skills/`.
4. Write the test for a "Done when" check, then the code.
5. Run the quality gate. Name the requirement ID in the pull request title.

With an AI harness the steps are the same: point it at `CLAUDE.md` or `AGENTS.md`, name the unit, and review its output against the "Done when" checks and the security skill.

## Repository hygiene

- Never commit `.env` files, tokens or keys. `.gitignore` excludes them.
- Lockfiles (`uv.lock`, `apps/web/package-lock.json`) are committed.
- Line endings are LF; `.gitattributes` and `.editorconfig` enforce it on Windows.
