# Identity and SSO

Sources: `PE-AWS Single Sign-On-191126-055533.pdf` (SSO guide); `NAVEX VoC - Technical Architecture and Sizing.pptx` (Arch deck slides 2-5, 10, 13); `NAVEX_VoC_Cost_and_Infrastructure_by_Environment.xlsx` (Cost xlsx, Inventory rows 32-38, Checklist rows 10-12); `NAVEX_VoC_Platform_Architecture_Diagram.png`; `navex-voc-platform-scaffold.zip` (`SSO.md`).

## Already in docs/ (read there, not here)

- Developer AWS access (Corp AD -> IAM Identity Center, CLI v2 profile, `navexsso` session, no static keys): `docs/03-engineering/sso-and-aws-access.md` "Part 1". The SSO guide is copied at NAVEX's AWS Single Sign-On guide (PDF, outside this repository).
- Workspace sign-in: Entra registrations, the six `VoC.*` app roles, env variables, MSAL PKCE flow in code, token rules: `sso-and-aws-access.md` "Part 2".
- Roles, data scopes (`OWN_BOOK`, `TEAM`, `REGION`, `ALL`), `VOC_ROLE_MAP`: `docs/01-product/roles-and-access.md`.
- Decisions 7 (role and scope separate), 8 (tokens in memory), 14 (navexsso profiles): `docs/02-architecture/decisions.md`.

## What the sources add

### SSO guide details not in docs/

- Access covers consoles and programmatic tokens for CLI, AWS Tools for PowerShell, SDKs and Terraform, from the start page's "Command line or programmatic access" link.
- Alternatives to CLI v2: an internal PowerShell credential helper that writes env vars or `~/.aws/credentials`; the NAVEX CLI, updated for SSO via CLI v2.
- A "SSO Group Permissions" page lists accounts, group owners and permissions per group; "Managing SSO Groups" covers owner tasks.
- Non-PE staff: team lead requests Corp AD groups; escalation via an admin-requests channel.
- Resolved history: a group-size paging bug (over 100 users) fixed by AWS; hosting groups moved to owner management.

### Per-environment Entra setup (Cost xlsx Inventory)

| Item | DEV | QA | Staging | Prod |
|---|---|---|---|---|
| SPA registration | PKCE, single tenant, redirect to the env URL | same | same | same |
| API registration | scope `access_as_user` | same | same | plus web app pre-authorised |
| App roles | 6 `VoC.*` roles | same | same | same |
| Enterprise app user assignment (required) | project team | QA testers | UAT testers | CXMs, leaders, AEs, ELT, VoC admins by role |
| Graph `User.Read.All` (application, admin consent) | yes | yes | yes | yes |
| Conditional Access | NAVEX standard | standard | standard | standard incl. MFA |
| Tenant and client ids | shared with the delivery team | same | same | in deployment configuration |

Rationale recorded: app roles put "role carried in the token, so access needs no group lookup" (row 34). An unassigned user is refused (row 35).

### Role model across phases

| Phase | Roles (Arch deck slides 2-4; Platform diagram) |
|---|---|
| MVP | CXM, CXM leadership, AE, ELT, VoC admin (deck: five roles; docs/ maps six app roles incl. AE leader) |
| Phase 1 | Product, Product leadership; "Product roles added in Entra ID" (Checklist row 19); entitlements extended to Product, AE, ELT, business roles (Roadmap png) |
| Phase 2 | Business teams: Marketing, Finance, RevOps, Sales; Executive, Finance and Sales views |

Identity and access blocks (Platform diagram): NAVEX enterprise SSO; group and role sync (directory groups -> platform roles); RBAC policy (scope: own book, team, region or all); entitlement service (role and scope resolved on every request); PII protection on every output; one policy inherited by both front doors (web and agents).

### Machine and agent identity

| Identity | Phase | Mechanism (Arch deck slide 10; Cost xlsx) |
|---|---|---|
| Refresh Agent workload identity | MVP | AgentCore Identity for calls to Enterpret MCP and Snowflake; credentials in Secrets Manager, no keys in code |
| Service account (`voc-insights` mailbox) | MVP | Signs in to Enterpret (MCP token) and sends alerts; one Prod, one non-prod shared by DEV, QA, Staging |
| Snowflake service user | MVP | Key pair, read role |
| Insights agent user pass-through | Phase 1 | AgentCore Identity federated with Entra ID; Gateway tools carry the user's identity so the API enforces scope |
| GitHub Actions deploy | MVP | OIDC to an AWS deploy role, no stored keys |

Scaffold principle (`SSO.md`): a scheduled run has no user; it runs with platform scope and writes rows carrying ownership columns; every human read goes back through a user scope.

### Scaffold design points not in docs/ (`SSO.md`)

- Entra caps group claims at about 200 and then emits a `_claim_names` pointer; the resolver must read groups from the directory and distinguish empty from failed resolution.
- Cache: signing keys until an unknown key id; resolved scope 5 min (subject + groups hash); ownership master 5 min. Revocation delay equals the scope cache window.
- Open in the scaffold: acceptable revocation delay; who may see verbatim text (a role flag needing a policy owner).

## Conflicts with docs/

| # | Topic | Sources | docs/ |
|---|---|---|---|
| 1 | Claim used for role | Scaffold: groups claim with directory overflow fallback; Cost xlsx: app roles in the token | Either app roles or `groups` claim; first match wins (`roles-and-access.md` "Mapping Corp AD to roles"); overflow not handled in docs |
| 2 | Where scope is enforced | Platform diagram and deck slides 3-4: "row and column security applied in the data platform" | Scope bound into the PostgreSQL query by the API (`roles-and-access.md` "Data scopes"; `decisions.md` 7) |
| 3 | Scope cache | Scaffold: 5-minute scope cache | `hld.md` 9: "cached briefly", no figure |
| 4 | MVP role count | Deck slide 4: five roles | Six app roles incl. `VoC.AELeader` (`sso-and-aws-access.md` Part 2) |

## Open questions

- App roles or groups claim: NAVEX IT to confirm (Checklist row 10, "process" with DevOps).
- Acceptable revocation delay, hence scope cache window.
- Product and business role names and scopes for Phase 1 and 2.
- AgentCore Memory retention ("set by NAVEX policy", deck slide 10).
