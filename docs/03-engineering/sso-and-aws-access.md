# SSO and AWS access

Two separate uses of the same identity provider. Corp AD (Microsoft Entra ID) is NAVEX's identity provider for both.

| Use | Who | Mechanism |
|---|---|---|
| Signing in to the workspace | Every user | OpenID Connect from the browser with MSAL; the API validates the token |
| Working with AWS as a developer | The delivery team | AWS IAM Identity Center (AWS SSO) federated to Corp AD, through AWS CLI v2 named profiles |

## Part 1: developer access to AWS

Source: NAVEX's "AWS Single Sign-On" guide (PDF, held outside this repository).

IAM users have been replaced with federated users. Users are placed in Corp AD groups, and each group maps to roles in target AWS accounts.

### Get access

1. Product Engineering staff are added to the `SG-Technology - PE` group during Corp onboarding. If the start page does not work, raise a KACE ticket for Internal IT to add you to that group; your team lead can help.
2. For any other group, the group owner adds you in the Azure web console. Owners are not members automatically and must add themselves.
3. Open `https://navexglobal.awsapps.com/start` and confirm you can see the accounts you expect.

### Configure AWS CLI v2

Remove AWS CLI v1 completely first, then install v2. `aws --version` must report 2.x.

Run `aws configure sso --profile navexdev` and answer:

| Prompt | Value |
|---|---|
| SSO session name | `navexsso` |
| SSO start URL | `https://navexglobal.awsapps.com/start` |
| SSO region | `us-west-2` |
| SSO registration scopes | `sso:account:access` |

Use the same session name for every NAVEX profile so they share one sign-in. The result in `~/.aws/config` looks like `scripts/aws-config.example`.

### Daily use

```bash
aws sso login --profile navexdev
aws s3 ls --profile navexdev --region us-west-2
```

- Name the profile on every command. The default profile can point anywhere.
- Add `--region` for anything that is not global.
- For the services in this repository, set `AWS_PROFILE=navexdev` and `AWS_REGION=us-west-2` in your `.env`; `boto3` picks them up.
- Never create or commit static IAM access keys.

Help: the `#aws-sso` channel.

## Part 2: sign-in for the workspace

### What NAVEX IT registers, per environment

| Item | Value |
|---|---|
| App registration: SPA | Platform "Single-page application". Redirect URIs: the environment's URL and `http://localhost:5173` for DEV |
| App registration: API | Exposes scope `access_as_user`. Application ID URI `api://<api-client-id>` |
| Token configuration | Access token v2. Either app roles (`VoC.CXM`, `VoC.CXMLeader`, `VoC.ELTViewer`, `VoC.AE`, `VoC.AELeader`, `VoC.Admin`) assigned to Corp AD groups, or the `groups` claim |
| Graph permission | `User.Read.All` (application) for the org chart sync |
| Conditional Access | NAVEX's standard policy |

Group membership is managed by group owners in the Azure web console. The application has no user management.

### Values the code needs

| Variable | Used by | Example |
|---|---|---|
| `VITE_ENTRA_TENANT_ID` | Web | Tenant GUID |
| `VITE_ENTRA_CLIENT_ID` | Web | SPA client ID |
| `VITE_API_SCOPE` | Web | `api://<api-client-id>/access_as_user` |
| `VITE_API_BASE_URL` | Web | `/api/v1` |
| `ENTRA_TENANT_ID` | API | Tenant GUID |
| `ENTRA_API_AUDIENCE` | API | API client ID |
| `VOC_ROLE_MAP` | API | JSON map of claim value to role and scope; see `01-product/roles-and-access.md` |

### The flow in code

1. `apps/web/src/lib/authConfig.ts` builds the MSAL configuration: authorization code with PKCE, cache in memory.
2. `features/auth/AuthProvider.tsx` starts MSAL, waits for it to initialise, and redirects to Entra when there is no account. The route the user asked for is kept, so deep links survive sign-in.
3. `lib/apiClient.ts` calls `acquireTokenSilent` before each request and sets `Authorization: Bearer <token>`. On `401` it retries once after a fresh silent token, then falls back to a redirect. On `403` it raises an access-denied notice and keeps the session.
4. `services/experience-api/app/core/security.py` checks signature, issuer, audience and expiry against Entra's published keys, cached in the process.
5. `core/entitlements.py` maps the token's `roles` and `groups` claims to a role and data scope and returns `CurrentUser`.
6. `GET /api/v1/me/entitlements` gives the browser the role, permissions and scope. The UI trusts that response, not the decoded token.

### Rules

- Tokens are never written to `localStorage` or `sessionStorage`, and never logged.
- The bearer token is never sent to S3. Presigned upload and download requests go out without it.
- Every route except `/health` and `/ready` requires a valid token.
