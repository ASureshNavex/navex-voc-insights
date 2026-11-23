# React handover: mockup to component mapping and the contracts it assumes

Sources: Artifacts/NAVEX_VoC_Mockup_React_Handover.md (Handover md, 16 Nov, sections s1 to s6), Artifacts/NAVEX_VoC_Insights_Workspace_Mockup.html (Handover mockup), NAVEX_VoC_Insights_Workspace_Latest.html (Latest, 19 Nov), Skill_Notes_Worked_Out.txt (Skill notes 19 Nov).

The Handover md describes the 16 Nov mockup, not the 19 Nov Latest prototype. Where they differ, Latest and docs/ win (`docs/01-product/requirements.md`, "Sources and precedence"). Use this file for the mapping method and component vocabulary, not for screen scope.

## Already in docs/ (do not restate)

- Stack, folder layout, permission guards, query keys, loaders, styling rules: `docs/03-engineering/coding-standards.md` and the seven skills it lists (Skill notes 19 Nov are their source text).
- Endpoint list, paging, errors, money and field-name conventions: `docs/03-engineering/api-contract.md`, Conventions.
- SPA module split and role-aware rendering: `docs/02-architecture/lld.md` 2.1.
- Component file names per requirement: `docs/01-product/requirements.md`, Web / API column.

## How the mockup maps to React (Handover md s1)

| Mockup element | React equivalent |
|---|---|
| `:root` CSS variables (brand, primary, red, yel, grn, gry, radii, font) | Theme tokens; replace brand with the official NAVEX value |
| `api` object, one function per endpoint | One TanStack Query hook per endpoint over a typed fetch client |
| PascalCase function taking one props object | Function component, same name and props |
| `data-component` attribute | Component name (Annotations: React components) |
| `data-req` attribute | FRD or scope reference (Annotations: Requirement references) |
| `state.filters`, `state.sort`, `state.view` | URL search params; saved views and deep links share the format |
| `state.open`, `state.chart`, `state.menu` | Local `useState` |
| `data-action` handlers | Event props |
| `#account=<sfdc_id>&src=cta` | Route `/accounts/:sfdcAccountId?src=cta`, preserved through MSAL sign-in |

## Component vocabulary: Handover md vs docs/ and the repo

| Handover md (16 Nov) | docs/ requirement and repo name | Note |
|---|---|---|
| `App` (MSAL, QueryClient, router) | `App.tsx` | Provider order per front-end skill: MSAL, QueryClient, Entitlement, Router |
| `AppHeader` | `components/shared/AppShell.tsx` | Top bar with tabs and bell (decisions #15) |
| `WorkspacePage` at `/accounts` | `features/accounts/ScorecardPage.tsx` (SCR-01) | Label "Scorecard" |
| `WorkspaceHeader` | SCR-01 heading; SVW tabs; EXP-01 button | |
| `DeepLinkBanner` | AUT-06, ACC-07 | Must not reveal out-of-scope accounts |
| `SummaryTiles` | `RatingCards.tsx` (SCR-04, 05) | |
| `RiskTrendChart` | `WeekOverWeek.tsx` (SCR-07) | Two-week compare, not 8 weeks |
| `PortfolioBreakdown` | `SegmentCards.tsx` (SCR-06) | |
| `FilterBar` | `FilterBar.tsx` (ACC-06) | |
| `AccountsTable`, `AccountRow` | `AccountsTable.tsx` (ACC-01, 02) | |
| `AccountDetail` | `AccountDetail.tsx` (ACC-07 to 12) | Expands in place |
| `AccountBriefDialog` | `AccountBriefDialog.tsx` (ACC-13) | |
| `SaveViewDialog` | `features/saved-views` (SVW) | |
| `DigestPreferencesDialog` | `DigestPreferences.tsx` (DIG-07) | Absent from Latest |
| `AdminPage` with Refresh and sources, Digests, Usage and audit, Access tabs | Separate admin pages (ADM, DIG, KHB) | Latest splits them into nav items |
| Later: `ProductWorkspace`, `DomainFrictionTable`, `DomainDeepDive`, `TopicResearch`, `KnowledgeHub`, `FactBase`, `FourQuadrantFactBase`, `EnterpriseViews`, `CreateCtaAction`, `ScopeTable` | Not MVP | Except the admin knowledge hub, now MVP (KHB) |

Shared primitives named in the Handover md: `RatingChip`, `ThemeChip`, `StatusTag` (New red, Repeat red, New yellow, Improved, Churn language), `InfoTip` (the (i) tooltip), `Delta`, `Dialog`, `Toast`, `Pill`. Latest adds a rule chip per trigger code (ACC-04).

## Data contract the Handover mockup expects (Handover md s3)

| Type | Fields (abridged) |
|---|---|
| `Rating` | R, Y, G, N (N = Gray, too little feedback; to confirm) |
| `AppRole` | VoC.CXM, VoC.CXMLeader, VoC.ELTViewer, VoC.AE, VoC.AELeader, VoC.Admin |
| `Me` | name, title, appRole, scopeSize, canFilterTeam |
| `PortfolioSummary` | red and yellow counts and ARR, prior week of each, newRed and newYellow lists, ratingCounts, lastRefresh, nextRefresh (ISO 8601) |
| `TrendPoint` | weekStart, total, red and yellow ARR and counts |
| `BreakdownRow` | label, count, red, yellow, total, red and yellow ARR |
| `Theme` | themeId, name, path (Enterpret taxonomy, no custom layer), volume, negative, isPrimary |
| `Verbatim` | id, text, source, date, theme, citationUrl optional |
| `AccountRow` | sfdcAccountId, name, segment, team, region, arr, arrTier, nextRenewal, product, superProductFamily, productIssue (Open, In progress, Resolved, None), cxm, ae, execSponsor, rating, previousRating, firedRule, confidence (High, Medium, Low), churnLanguage, churnScore, churnScoreAsOf, themes, topVerbatim |
| `AccountDetail` | AccountRow plus explanation and driverVerbatims |
| `AccountFilters` | status, q, segment, theme, renewalWithinDays (90, 180, 365), arrTier, region, family, issue, churnLanguage, team, cxm, flag (newred, newyel), sort (arr, renewal, rating, churn) |

Money is USD thousands in the mockup; the API returns whole dollars (Handover md s3).

## Behaviour notes for the build (Handover md s5)

- Charts: Recharts or visx; the mockup draws plain SVG. Labels sit on bars; current week labelled "This week".
- Excel comes from the API; client-side export (SheetJS) only if NAVEX asks. The export carries metadata rows: exported by, time, filters, data as of (Handover mockup).
- Table: account cell has a left rail in the rating colour; rows expand in place; theme chips show negative counts, full taxonomy path in the title and detail.
- Tooltips: VoC rating and churn score (i) tooltips reachable by keyboard focus; text to be confirmed.
- Accessibility: visible focus, labelled controls, rating as text as well as colour, reduced motion, works at 390 px.
- Logo: header reads the official NAVEX logo file and falls back to the text "NAVEX"; never redraw it. Latest embeds the SVG.
- Scope is enforced by the API on every call; role-aware UI is presentational only (Handover md s4).

## Conflicts with docs/

| Topic | Handover md / mockup | docs/ |
|---|---|---|
| Identity endpoint | `GET /me` returning appRole and canFilterTeam | `GET /api/v1/me/entitlements` with role, permissions, data scope, scope size; UI checks permissions only (`docs/01-product/roles-and-access.md`) |
| Path prefix | Endpoints without a version prefix | Everything under `/api/v1` (`docs/03-engineering/api-contract.md`) |
| Query keys | `["accounts", filters]`, `["summary"]` | Must include data scope: `["accounts", dataScope, filters]` (coding-standards, Query keys) |
| Field casing | camelCase types (`sfdcAccountId`) | snake_case on the wire, kept as returned (api-contract, Conventions) |
| Money type | `arr: number` in whole dollars | Whole US dollars as decimal strings |
| Trend endpoint | `GET /portfolio/trend?weeks=8`, 8-week series | SCR-07 compares last week with this week |
| Default sort and renewal filter | sort `arr`; renewalWithinDays 90/180/365 | ACC-14 churn-language first; ACC-06 window within or beyond 180 days |
| Churn score placement | Column in the table and in the export | ACC-01 has no churn score column; ACC-09 shows it in detail |
| Issue status values | Open, In progress, Resolved, None | Red - Open issue, Red - No open issue, Churn language - No issue, No flag (from Latest); mapping open item #10 |
| Theme tokens | `theme.css` or a tokens module | SCSS variables mapped to shadcn CSS variables (decisions #11) |
| Admin structure | One `/admin` page with four tabs | Separate admin pages per Latest (ADM, DIG, KHB) |
| Out-of-scope deep link | "Access message" naming the account | Same not-found response as an unknown account (AUT-06) |
