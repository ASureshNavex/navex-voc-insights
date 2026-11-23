# Experience API

FastAPI service behind `/api/v1`. It reads the published run from PostgreSQL and binds the caller's data scope into every query.

```bash
cp .env.example .env
uv run uvicorn app.main:app --reload --port 8000    # from this folder
```

Open `http://localhost:8000/docs` for the contract.

```text
app/
├── core/        config, security (token), entitlements (role, permissions, scope),
│                database, pagination, audit, telemetry, exceptions
├── domains/     one folder per capability: router.py, schemas.py, service.py
├── ports/       outbound adapters (S3 document store)
└── main.py      app factory, /health, /ready
```

## What is built

| Domain | Status |
|---|---|
| `me` | Built: `GET /me/entitlements` |
| `accounts` | Built: list with filters, sort and paging; detail. Contract only: Excel export, brief |
| `portfolio` | Built: summary. Contract only: trend |
| `saved_views` | Built: list, create, rename, delete |
| `knowledge_hub` | Status rules built and tested. Endpoints are contract only |
| `leadership`, `admin`, `digests`, `notifications` | Contract only |

A contract-only endpoint has its route, permission guard and schemas, and returns `501` with the requirement ID. Build it by writing `service.py` and replacing the `raise NotBuilt(...)` line. The accounts domain is the pattern to follow.

## Rules

- Every service function takes `CurrentUser` and applies `scope_filter(user.access_scope)`.
- Routers hold no SQL. Services return schemas, never ORM rows.
- Lists take `PageParams`; the cap is 200 and ordering ends with a unique column.
- Mutations call `record_audit` on the same transaction.
