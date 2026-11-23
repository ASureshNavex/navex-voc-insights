---
name: navex-fastapi-rest-apis
description: The Experience API and Python service conventions - FastAPI layout, Pydantic v2 contracts, Entra ID JWT validation, CurrentUser and scope_filter on every query, async database and HTTP patterns. Use when working under services/experience-api, services/ingestion or services/notifications; read building-an-endpoint.md beside it when building a Contract only endpoint.
---

# Python REST APIs (FastAPI): Engineering Skill

When building, refactoring, or reviewing any **FastAPI REST API** service across the platform, strictly follow this lean, domain-oriented architecture, security model, and quality standard.

---

## 1. Approved Stack & Quality Gate
- **Runtime & Framework:** Python 3.13, FastAPI, Pydantic v2 (strict validation & settings)
- **Database & Migrations:** SQLAlchemy 2.0 (`asyncio` + `asyncpg`) for PostgreSQL, Alembic for schema migrations
- **Outbound HTTP & Cloud SDKs:** `httpx` (`AsyncClient`) for internal/external service calls; `boto3` for AWS integrations
- **Tooling & CI Quality Gate:** `uv` (dependency & lockfile management), `ruff` (linting + formatting), `mypy` (strict static typing), `pytest` + `pytest-asyncio`, `pip-audit`, and `trivy`
- **Design Principle:** Keep API services **stateless, thin, and lean**. Offload scheduled jobs, long-running pipelines, and AI orchestration to dedicated background workers or AgentCore runtimes.

---

## 2. Lean Domain-Driven Folder Structure
Organize every API service by business domain under `app/` so routers, schemas, services, and data access stay colocated without unnecessary abstraction layers:

```text
<api-service>/
|-- alembic/                  # Database migration scripts
|-- app/
|   |-- core/                 # Service-wide infrastructure
|   |   |-- config.py         # Pydantic BaseSettings (env vars / AWS Secrets Manager)
|   |   |-- security.py       # Corp AD / Entra ID OIDC JWT verification (JWKS cache)
|   |   |-- entitlements.py   # Role & data-scope resolution dependencies
|   |   |-- database.py       # Async SQLAlchemy engine & session dependency
|   |   |-- telemetry.py      # OpenTelemetry tracing, metrics & structured JSON logging
|   |   `-- exceptions.py     # Global RFC 7807 / standardized JSON error handlers
|   |-- domains/              # Business capability modules
|   |   `-- <domain>/
|   |       |-- router.py     # HTTP routes, status codes, FastAPI dependencies
|   |       |-- schemas.py    # Strict Pydantic v2 Request/Response models
|   |       `-- service.py    # Business logic & scoped database queries
|   |-- ports/                # Thin outbound adapters (S3, MCP, downstream APIs)
|   `-- main.py               # FastAPI app factory, lifespan, versioned (/api/v1) router mount
|-- tests/                    # pytest suites (auth/RBAC tests, contract tests, service tests)
|-- pyproject.toml            # uv, ruff, mypy, and pytest configuration
`-- Dockerfile                # Minimal Python 3.13 container image
```

---

## 3. Authentication, RBAC & Data-Scope Enforcement
- **Zero Unauthenticated Endpoints:** Validate `Authorization: Bearer <token>` against Corp AD / Entra ID OIDC discovery keys (JWKS) on every route except `/health` and `/ready`.
- **Single-Resolution Identity Dependency:** Resolve the caller's identity, Corp AD groups, role, and access scope once per request via `Depends(get_current_user)`.
- **Mandatory Query Scope Binding:** Every database query or downstream fetch in `domains/*/service.py` **must** accept the resolved `CurrentUser` context and bind their access scope directly into the SQLAlchemy `WHERE` clause. Unscoped queries are forbidden.
- **Explicit Permission Guards:** Protect mutating or administrative endpoints with declarative permission dependencies (e.g., `Depends(require_permission("resource:write"))`).
- **Local AWS SSO Credentials:** Never use static IAM access keys. Local development must authenticate via AWS CLI v2 named profiles (`AWS_PROFILE=navexdev`, `AWS_REGION=us-west-2`, `sso_session = navexsso`).

---

## 4. API Contracts, Async I/O & Performance
- **Versioned Routes & REST Semantics:** Mount all endpoints under `/api/v1/...` using standard HTTP verbs, plural resource nouns, and accurate HTTP status codes (`200`, `201`, `204`, `400`, `401`, `403`, `404`, `422`).
- **Strict Pydantic v2 Boundaries:** Never return raw SQLAlchemy ORM models from routes. Define explicit `Request` and `Response` schemas (`ConfigDict(from_attributes=True)`).
- **Pagination by Default:** All list endpoints returning collections must enforce bounded pagination (`limit` with a strict max cap, `offset` or cursor) and deterministic ordering.
- **Non-Blocking I/O:** Use `async def` routes with `AsyncSession` and `httpx.AsyncClient` (configured with explicit connection/read timeouts). Offload CPU-bound tasks (e.g., `.xlsx` or CSV serialization) via `asyncio.to_thread()`.
- **Direct-to-Storage File Transfers:** Never proxy large file uploads or downloads through API memory. Issue short-lived S3 presigned URLs via a `ports/` adapter.

---

## 5. Observability & Error Handling
- **OpenTelemetry Instrumentation:** Propagate trace context (`traceparent`) across inbound requests, SQLAlchemy queries, and outbound `httpx` calls. Never log raw JWTs, secrets, or sensitive PII.
- **Consistent Error Payloads:** Catch domain exceptions globally in `core/exceptions.py` and map them to clean, predictable JSON error responses without leaking stack traces.
