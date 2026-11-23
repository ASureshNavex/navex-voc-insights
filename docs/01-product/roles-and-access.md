# Roles and access

Access has three parts, resolved on the server for every request and returned to the browser by `GET /api/v1/me/entitlements`.

| Part | Question it answers | Source |
|---|---|---|
| Role | What kind of user is this? | Corp AD group or app role in the token |
| Permissions | Which features can they use? | Role policy in `services/experience-api/app/core/entitlements.py` |
| Data scope | Which accounts can they see? | Role policy plus account ownership and the org chart |

The UI checks permissions, never role names: `<Can perform="knowledge_hub:upload">` or `usePermission("digests:manage")`.

## Roles

| Role | Label in the product | Data scope | MVP modules |
|---|---|---|---|
| `CXM` | CXM user | `OWN_BOOK` on CXM ownership | Scorecard, account brief, saved views, notifications |
| `CXM_LEADERSHIP` | CXM leadership | `TEAM` on CXM ownership | Scorecard with team filters and week over week, manager summary, custom reports, saved views, notifications |
| `ELT` | ELT viewer | `ALL`, read only | To be decided |
| `ACCOUNT_EXECUTIVE` | Sales (AE) | `OWN_BOOK` on AE ownership | To be decided |
| `ACCOUNT_EXECUTIVE` with a team | Sales leadership | `TEAM` on AE ownership | To be decided |
| `VOC_ADMIN` | VoC admin | `ALL` | Admin home, weekly changes, knowledge hub, data source health, usage and audit, digests, notifications |

Sales leadership is the Account Executive role with the `TEAM` scope. It is a separate Corp AD group mapped to the same role with a wider scope, which is why role and scope are separate fields.

## Data scopes

| Scope | Accounts returned |
|---|---|
| `OWN_BOOK` | Accounts where the user is the owner in the role's ownership field |
| `TEAM` | Accounts owned by the user or by anyone below them in the org chart |
| `REGION` | Accounts in the user's region. Reserved; no MVP role uses it |
| `ALL` | Every account |

The filter is built once in `packages/voc-data/src/voc_data/scope.py` and applied in every query. An account outside scope returns `404`, the same as an account that does not exist.

## Permissions

| Permission | CXM | CXM leadership | VoC admin |
|---|---|---|---|
| `scorecard:read` | Yes | Yes | |
| `scorecard:filter_team` | | Yes | |
| `scorecard:trend` | | Yes | |
| `scorecard:export` | Yes | Yes | |
| `account_brief:generate` | Yes | | |
| `saved_views:manage` | Yes | Yes | |
| `digest_preferences:manage` | Yes | Yes | |
| `notifications:read` | Yes | Yes | Yes |
| `manager_summary:read` | | Yes | |
| `custom_reports:manage` | | Yes | |
| `admin_home:read` | | | Yes |
| `weekly_changes:read` | | | Yes |
| `weekly_changes:email` | | | Yes |
| `knowledge_hub:upload` | | | Yes |
| `knowledge_hub:approve` | | | Yes |
| `source_health:read` | | | Yes |
| `source_health:check` | | | Yes |
| `usage_audit:read` | | | Yes |
| `digests:manage` | | | Yes |
| `access_list:read` | | | Yes |

ELT viewer and both Sales levels sign in and get a role and scope, with no permissions until NAVEX decides their modules. They see a page that says so.

## Mapping Corp AD to roles

The API reads the `roles` claim (Entra app roles) and the `groups` claim from the access token and maps the first match to a platform role. The mapping is configuration: `VOC_ROLE_MAP` in the API environment, a JSON object of claim value to role and scope.

```json
{
  "VoC.CXM": {"role": "CXM", "scope": "OWN_BOOK"},
  "VoC.CXMLeader": {"role": "CXM_LEADERSHIP", "scope": "TEAM"},
  "VoC.ELTViewer": {"role": "ELT", "scope": "ALL"},
  "VoC.AE": {"role": "ACCOUNT_EXECUTIVE", "scope": "OWN_BOOK"},
  "VoC.AELeader": {"role": "ACCOUNT_EXECUTIVE", "scope": "TEAM"},
  "VoC.Admin": {"role": "VOC_ADMIN", "scope": "ALL"}
}
```

Keys can be app role values, as above, or Corp AD group object IDs. NAVEX IT confirms which. Group membership is managed by group owners in the Azure web console; this application never edits it.

## Adding an access level

1. Add the Corp AD group or app role and its entry in `VOC_ROLE_MAP`.
2. If it needs a new set of features, add a role and its permissions in `core/entitlements.py` and in `apps/web/src/features/auth/permissions.ts`.
3. Add its row to this file and to `requirements.md`.
