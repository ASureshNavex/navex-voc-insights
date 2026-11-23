---
name: navex-security-code-review
description: Blocking security and reliability review across the web app, the API, the tasks and the agent - OWASP issues, SQL injection, unparameterized queries, missing scope or permission checks, unbounded lists, prompt injection. Use before calling any change done, as the last step of sgivp Verify, or when asked to review a diff.
---

# Security & Quality Code Review Skill (OWASP, SQLi, RBAC & Pagination)

When reviewing pull requests, auditing existing code, or verifying newly generated modules across the platform, systematically inspect the code against every checklist below. **Flag any violation as a blocking issue** with a concrete remediation snippet.

---

## 1. SQL Injection & Database Query Safety (CRITICAL)
- **Parameterized Queries Only:** Reject any SQL query built via Python f-strings, `%` formatting, `.format()`, or string concatenation (`+`). Enforce SQLAlchemy ORM expressions (`select(...).where(...)`) or bound parameters (`text("SELECT ... WHERE id = :id").bindparams(id=val)`).
- **Dynamic Identifiers (`ORDER BY` / Column Names):** Never interpolate user-supplied sort fields or table/column names directly into SQL. Validate sort keys against an explicit `Literal` / allowlist dictionary mapped to SQLAlchemy column objects.
- **Snowflake & MCP Queries:** Verify that any SQL sent to Snowflake or MCP data adapters uses bound query parameters (`%s` / `?` bindings) and never interpolates raw filter strings.

---

## 2. Authentication, RBAC & Broken Object Level Authorization (OWASP API1 / API5)
- **No Unauthenticated Endpoints:** Verify every FastAPI route enforces `Depends(get_current_user)` (Corp AD / Entra ID OIDC JWT validation) except explicit `/health` and `/ready` probes.
- **Mandatory Data-Scope Binding:** Confirm that every database query and downstream service call binds the caller's resolved `data_scope` (`OWN_BOOK`, `TEAM`, `REGION`, `ALL`) into the `WHERE` clause. Reject any endpoint that trusts a client-supplied `user_id`, `team_id`, or `region` without verifying it against the caller's entitlements.
- **Function-Level Authorization:** Verify mutating or administrative endpoints (approvals, run triggers, audit exports) enforce explicit permission checks (`Depends(require_permission(...))`).
- **Front-End Token Hygiene:** Flag any usage of `localStorage` or `sessionStorage` for storing JWTs or session tokens.

---

## 3. Pagination, Resource Limits & DoS Prevention (OWASP API4)
- **Strict Bounded Pagination:** Reject any list endpoint or database query (`SELECT *`) that lacks a `LIMIT` clause or allows unbounded `limit` values. Enforce Pydantic field constraints (`limit: int = Field(default=50, ge=1, le=200)`, `offset: int = Field(default=0, ge=0)`).
- **Deterministic Ordering:** Ensure every paginated query includes a deterministic `ORDER BY` clause (including a unique tie-breaker column such as `id`) so rows never duplicate or skip across pages.
- **Outbound Timeouts & Payload Caps:** Verify every `httpx.AsyncClient` and `boto3` call defines explicit connect/read timeouts, and file uploads use size-limited S3 presigned URLs rather than buffering files in API memory.

---

## 4. OWASP Web, XSS & Injection Defenses
- **Cross-Site Scripting (XSS):** Flag any use of `dangerouslySetInnerHTML`, unescaped HTML rendering in Jinja2 email templates (`| safe`), or unvalidated URLs in `href={...}` (block `javascript:` URIs).
- **SSRF Prevention (OWASP API7):** Reject any backend endpoint or worker that fetches arbitrary user-supplied URLs. Outbound HTTP clients must only connect to allowlisted internal hosts or configured AWS service endpoints.
- **No Secrets or PII in Code/Logs:** Flag hardcoded API keys, AWS credentials, tokens, or connection strings. Verify OpenTelemetry logs and exception handlers redact `Authorization` headers, JWTs, and sensitive customer verbatim PII.

---

## 5. AI & AgentCore Security (OWASP LLM Top 10)
- **Prompt Injection Separation:** Verify untrusted external data (customer verbatim text, uploaded Knowledge Hub documents) is clearly delimited inside `.j2` Jinja2 templates (e.g., wrapped in `<verbatim_data>...</verbatim_data>` tags) with explicit grounding instructions to treat it strictly as data, never instructions.
- **Structured Output Validation:** Confirm Bedrock responses are parsed through strict Pydantic v2 schemas (`with_structured_output`) before saving to PostgreSQL or rendering in the UI.
- **Memory & Knowledge Base Isolation:** Verify AgentCore Memory namespaces and Bedrock Knowledge Base retrieval filters enforce the caller's RBAC `data_scope`.

---

## 6. Automated Tooling & Dependency Hygiene
Before approving any change, verify compliance with the platform quality gate:
- **Python:** `ruff check`, `mypy --strict`, `pytest`, and `pip-audit` (zero high/critical CVEs).
- **Front End:** `tsc --noEmit` (strict TypeScript 5), `eslint`, and `npm audit`.
- **Containers:** `trivy` image scan passes with zero unpatched critical vulnerabilities, and containers run as a non-root user.

---

## Review Output Format
When reporting findings, categorize issues by severity:
1. **[BLOCKER - SECURITY]:** SQLi, missing RBAC scope, auth bypass, secret leak, XSS, SSRF.
2. **[BLOCKER - RELIABILITY]:** Unbounded pagination, missing timeouts, non-idempotent worker writes.
3. **[WARNING - HARDENING]:** Missing tie-breaker sort in pagination, overly broad exception catches, missing unit tests.
