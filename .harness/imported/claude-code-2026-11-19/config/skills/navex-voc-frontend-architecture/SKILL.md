---
name: navex-voc-frontend-architecture
description: Enforces React 19, TypeScript 5, Vite, Corp AD / Entra ID & AWS SSO federation, RBAC data-scoping, TanStack Query/Table, FastAPI JWT integration, and Tailwind/shadcn/SCSS styling for the NAVEX VoC Enterprise Platform.
---

# NAVEX VoC Enterprise Platform — Front-End Skill

When generating, refactoring, or reviewing front-end code for the **NAVEX VoC Enterprise Platform**, strictly adhere to the technology stack, Corp AD / AWS SSO federation conventions, RBAC data-scoping rules, API contracts, and UI styling guidelines below.

---

## 1. Approved Front-End Stack
- **Core:** React 19, TypeScript 5 (strict mode), Vite
- **Identity & SSO:** Corp AD (Microsoft Entra ID) federated with AWS SSO (`@azure/msal-react` and `@azure/msal-browser` for browser OIDC tokens; AWS CLI v2 `navexsso` session for local developer AWS access)
- **Server State & Data Grids:** `@tanstack/react-query` (v5) and `@tanstack/react-table` (v8)
- **UI & Styling:** Tailwind CSS, `shadcn/ui` (MIT-licensed primitives), and Parameterized SCSS partials (`src/styles/`)
- **Prohibited Libraries:** Do **not** install Redux, Redux Toolkit, or external heavy component libraries (e.g., MUI, Ant Design).

---

## 2. Feature-Based Codebase Structure
Organize code strictly by business domain aligned with the platform's capability modules:

```text
src/
├── assets/                   # Static assets and brand media
├── components/
│   ├── ui/                   # Pure shadcn/ui primitives (no business logic or auth hooks)
│   └── shared/               # Reusable app components (<Can />, <PageLoader />, <DataTable />)
├── features/
│   ├── auth/                 # Corp AD / Entra ID MSAL setup, AuthProvider, useEntitlements, <ProtectedRoute />
│   ├── accounts/             # Account views, health/churn scores, ARR & renewal summaries
│   ├── themes/               # Taxonomy themes, verbatim feedback explorer, filters
│   ├── knowledge-hub/        # Leadership document uploads (S3 presigned), file checks, approvals
│   ├── saved-views/          # Private saved filter views and Excel (.xlsx) export triggers
│   ├── digests/              # Notification & email digest preferences
│   └── admin/                # VoC Admin workspace, run control, usage & audit logs
├── lib/
│   ├── authConfig.ts         # Corp AD / Entra ID OIDC configuration
│   ├── apiClient.ts          # Typed HTTP client with Bearer JWT interceptor & error handling
│   └── utils.ts              # cn() class-merging helper
├── routes/                   # Lazy-loaded route definitions with RBAC guards
├── styles/
│   ├── _variables.scss       # Parameterized theme knobs (\$brand-hue, radius, sidebar-width)
│   ├── _themes.scss          # Maps SCSS variables to shadcn/ui CSS custom properties
│   ├── _mixins.scss          # Responsive and surface mixins
│   ├── _loaders.scss         # Standardized CSS spinner & skeleton animations
│   └── main.scss             # Tailwind entry + partial imports
└── App.tsx                   # AuthProvider (MSAL) -> QueryClientProvider -> EntitlementProvider -> Router
```

---

## 3. Authentication (Corp AD / AWS SSO) & FastAPI JWT Integration
- **Federated Identity Flow:** Corp AD (Azure / Entra ID) acts as the central Identity Provider (IdP) for both browser OIDC authentication and AWS SSO (`https://awsapps.com`).
- **Token Acquisition:** Never store JWTs in `localStorage` or `sessionStorage`. Acquire OIDC access tokens silently in memory via `instance.acquireTokenSilent()` inside `src/lib/apiClient.ts`.
- **Experience API Contract (`FastAPI`):**
  - Route all REST calls through `apiClient` to the versioned Experience API (`/api/v1/...`).
  - Attach `Authorization: Bearer <oidc_token>` automatically via request interceptors so the Experience API can validate the token and bind the user's AD group/access scope into every query.
  - Handle `401 Unauthorized` by triggering `acquireTokenSilent` (falling back to `acquireTokenRedirect`), and `403 Forbidden` by surfacing a non-destructive Access Denied banner/toast.
- **S3 Presigned Uploads (Knowledge Hub):** For Knowledge Hub document uploads, request a presigned upload URL from the Experience API first, then `PUT` the file directly to S3 without attaching the Bearer header to the S3 request.
- **Local Developer AWS Access:** When generating scripts, local tooling, or environment documentation for developers interacting with AWS resources (S3, Bedrock, RDS), always reference AWS CLI v2 named profiles (`--profile <name> --region us-west-2`) backed by `sso_session = navexsso` and `sso_registration_scopes = sso:account:access`—never static IAM access keys.

---

## 4. RBAC & Corp AD Group Data-Scope Enforcement
Users are placed in Corp AD groups (managed via Azure Web Console by group owners; `SG-Technology - PE` for Product Engineering) which map to **five platform roles** and **four data scopes**:
- **Roles:** `CXM`, `CXM_LEADERSHIP`, `ACCOUNT_EXECUTIVE`, `ELT`, `VOC_ADMIN`
- **Data Scopes:** `OWN_BOOK`, `TEAM`, `REGION`, `ALL`

### Rules:
1. **Entitlement Resolution:** Do not rely solely on raw AD group IDs in the front end. Fetch the resolved platform role, granular permissions, and active data scope from `/api/v1/me/entitlements` upon login and cache via TanStack Query.
2. **Permission-Based UI Guards:** Never hardcode role or AD group checks (`role === 'VOC_ADMIN'`) inside UI components. Use declarative permission checks via `<Can perform="knowledge_hub:approve">` or `usePermission('run_control:execute')`.
3. **Scope-Aware Query Keys:** Always include the user's `dataScope` and active filter parameters in TanStack Query keys (e.g., `['accounts', dataScope, filters]`) so cached data never leaks across scope changes.
4. **Bundle Splitting:** Lazy-load `VOC_ADMIN` routes (Run Control, Usage & Audit) using `React.lazy()` and `<Suspense fallback={<PageLoader />}>`.

---

## 5. TanStack Query & Table Conventions
- **Server State:** Use `@tanstack/react-query` for all Experience API endpoints (accounts, themes, verbatim, briefs, saved views).
- **Data Tables & Excel Export:**
  - Build all tabular views (Accounts, Verbatim, Audit Logs) using `@tanstack/react-table` + shadcn `<Table>`.
  - Support server-side pagination, sorting, and filtering aligned with FastAPI query parameters.
  - When triggering **Excel downloads**, send the active table filter state to the Experience API export endpoint and stream the `.xlsx` blob response cleanly.

---

## 6. UI Styling, Parameterized SCSS & Loaders
- **Zero Inline Styles:** Inline `style={{ ... }}` attributes are strictly forbidden. Use Tailwind CSS utilities or BEM-style classes defined in `src/styles/` partials.
- **Parameterized Theming:** Control brand colors, border radii, and layout dimensions via SCSS variables in `src/styles/_variables.scss` mapped to shadcn/ui CSS variables (`bg-background`, `bg-card`, `text-muted-foreground`, `border-border`) in `_themes.scss`. Never hardcode hex values in JSX.
- **Responsive Shell:** Use shadcn/ui's `<SidebarProvider>` and `<Sidebar>` for the single-front-door workspace (collapsible desktop rail + mobile `<Sheet>` drawer). Wrap tables in `overflow-x-auto` and apply `tabular-nums` to all ARR, CSAT, NPS, and churn figures.
- **Three-Tier Loaders:**
  1. `<PageLoader />` (SCSS `.loader-spinner`) for lazy route `<Suspense>` fallbacks.
  2. `<Skeleton />` matching widget/table row dimensions during TanStack Query initial fetches.
  3. `<ButtonLoader />` (`animate-spin`) inside disabled action buttons during mutations (e.g., saving views, triggering refresh runs, uploading documents).
