# API contract

All endpoints are under `/api/v1`, return JSON unless stated, and need a bearer token. `/health` and `/ready` are the only open routes. The live contract is at `/docs` on a running API; this table adds the build status.

| Status | Meaning |
|---|---|
| Built | Implemented and tested |
| Contract only | Route, permission guard and schemas exist; the handler returns `501` naming its requirement. Build it by writing the service function and replacing the `raise NotBuilt(...)` line |

| Area | Method | Path | Permission | Status | Requirement |
|---|---|---|---|---|---|
| me | GET | `/me/entitlements` | Any mapped role | Built |  |
| portfolio | GET | `/portfolio/summary` | `scorecard:read` | Built |  |
| portfolio | GET | `/portfolio/trend` | `scorecard:trend` | Contract only | SCR-07 |
| accounts | GET | `/accounts` | `scorecard:read` | Built |  |
| accounts | GET | `/accounts/export.xlsx` | `scorecard:export` | Contract only | EXP-01 |
| accounts | GET | `/accounts/{sfdc_account_id}` | `scorecard:read` | Built |  |
| accounts | GET | `/accounts/{sfdc_account_id}/brief` | `account_brief:generate` | Contract only | ACC-13 |
| saved views | GET | `/saved-views` | `saved_views:manage` | Built |  |
| saved views | POST | `/saved-views` | `saved_views:manage` | Built |  |
| saved views | PATCH | `/saved-views/{view_id}` | `saved_views:manage` | Built |  |
| saved views | DELETE | `/saved-views/{view_id}` | `saved_views:manage` | Built |  |
| notifications | GET | `/notifications` | `notifications:read` | Contract only | ALR-05 |
| notifications | POST | `/notifications/read` | `notifications:read` | Contract only | ALR-05 |
| leadership | GET | `/leadership/summary` | `manager_summary:read` | Contract only | LDR-01 to LDR-03 |
| leadership | GET | `/leadership/report-templates` | `custom_reports:manage` | Contract only | LDR-04 |
| leadership | POST | `/leadership/report-templates/{template_id}/run` | `custom_reports:manage` | Contract only | LDR-04 |
| leadership | GET | `/leadership/friction-report` | `custom_reports:manage` | Contract only | LDR-05 |
| knowledge hub | POST | `/knowledge-hub/uploads` | `knowledge_hub:upload` | Contract only | KHB-01 |
| knowledge hub | POST | `/knowledge-hub/files/{document_id}/complete` | `knowledge_hub:upload` | Contract only | KHB-02 |
| knowledge hub | GET | `/knowledge-hub/files` | `knowledge_hub:upload` | Contract only | KHB-03 |
| knowledge hub | GET | `/knowledge-hub/files/{document_id}/download` | `knowledge_hub:upload` | Contract only | KHB-03 |
| knowledge hub | DELETE | `/knowledge-hub/files/{document_id}` | `knowledge_hub:upload` | Contract only | KHB-04 |
| knowledge hub | POST | `/knowledge-hub/files/{document_id}/approve` | `knowledge_hub:approve` | Contract only | KHB-04 |
| knowledge hub | POST | `/knowledge-hub/files/{document_id}/decline` | `knowledge_hub:approve` | Contract only | KHB-04 |
| digests | GET | `/admin/digests` | `digests:manage` | Contract only | DIG-01 |
| digests | PATCH | `/admin/digests/{digest_id}` | `digests:manage` | Contract only | DIG-03 |
| digests | POST | `/admin/digests/{digest_id}/preview` | `digests:manage` | Contract only | DIG-04 |
| digests | POST | `/admin/digests/{digest_id}/send` | `digests:manage` | Contract only | DIG-04 |
| digests | GET | `/admin/digests/archive` | `digests:manage` | Contract only | DIG-05 |
| digests | GET | `/me/digest-preferences` | `digest_preferences:manage` | Contract only | DIG-07 |
| digests | PUT | `/me/digest-preferences` | `digest_preferences:manage` | Contract only | DIG-07 |
| admin | GET | `/admin/home` | `admin_home:read` | Contract only | ADM-01 |
| admin | GET | `/admin/weekly-changes` | `weekly_changes:read` | Contract only | ADM-02 |
| admin | POST | `/admin/weekly-changes/email` | `weekly_changes:email` | Contract only | ADM-03 |
| admin | GET | `/admin/source-health` | `source_health:read` | Contract only | ADM-04 |
| admin | POST | `/admin/source-health/check` | `source_health:check` | Contract only | ADM-04 |
| admin | GET | `/admin/refresh-runs` | `source_health:read` | Contract only | ADM-05 |
| admin | GET | `/admin/usage/highlights` | `usage_audit:read` | Contract only | ADM-06 |
| admin | GET | `/admin/usage` | `usage_audit:read` | Contract only | ADM-07 |
| admin | GET | `/admin/audit` | `usage_audit:read` | Contract only | ADM-08 |
| admin | GET | `/admin/access` | `access_list:read` | Contract only | ADM-09 |

8 of 41 operations are built.

## Conventions

| Topic | Rule |
|---|---|
| Scope | Every read is limited to the caller's data scope. Filters only narrow within it |
| Not found | An account outside scope returns `404`, the same as an unknown account |
| Paging | `limit` 1 to 200, default 50; `offset` from 0. Lists return `items`, `total`, `limit`, `offset` |
| Errors | `application/problem+json` with `title`, `status`, `detail`. `401` invalid token, `403` no mapped role or missing permission, `404`, `409` state conflict or duplicate name, `422` invalid input, `501` not built |
| Money | Whole US dollars as decimal strings |
| Dates | ISO 8601; timestamps in UTC |
| Field names | `snake_case` on the wire; the web app keeps them as returned |
