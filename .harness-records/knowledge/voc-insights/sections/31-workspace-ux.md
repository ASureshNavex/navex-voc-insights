# Insights Workspace UX: screens, navigation, states and version history

Sources: mockups `VoC Insights Workspace-Dec8.html` (Dec8, 12 Nov), `VoC Insights Workspace - MVP.html` (MVP v1, 13 Nov, the one NAVEX reviewed), `Artifacts/NAVEX_VoC_Insights_Workspace_Mockup.html` (Handover mockup, 16 Nov), `VoC Insights Workspace - Latest Feedback.html` (Latest Feedback, 19 Nov 12:44), `NAVEX_VoC_Insights_Workspace_Latest.html` (Latest, 19 Nov 13:19); Artifacts/NAVEX_VoC_Mockup_React_Handover.md (Handover md); engagement zip 00_INDEX.md; Skill_Notes_Worked_Out.txt (Skill notes).

## Where the current spec already lives (read these, not this file, for screen detail)

- Screen content, fields, filters, columns per screen: `docs/01-product/requirements.md`, sections SCR, ACC, SVW, EXP, ALR, LDR, ADM, DIG, KHB.
- Roles, scopes, permission matrix: `docs/01-product/roles-and-access.md`.
- Reference prototype and its demo-only controls: `docs/reference/prototype/README.md`.
- Removed screens and why: `docs/01-product/requirements.md`, "Removed from the MVP".
- Navigation pattern (top bar, bell): `docs/02-architecture/decisions.md` #15; `docs/01-product/open-items.md` #14.

## Version lineage

| Version | Date | Roles in role picker | What it is |
|---|---|---|---|
| Dec8 | 12 Nov | CXM user, CXM leadership, VoC admin | First wireframe; "Dec8" most likely names the MVP date (Phase 1 starts 9 Dec 2026, `docs/01-product/overview.md`, Phases); the file does not say |
| MVP v1 | 13 Nov | same three | Dec8 plus search, select filters and simulated "Download CSV" on the usage-by-segment and resolved-product-issues tables. Reviewed by NAVEX (Feedback 13 Nov) |
| Handover mockup | 16 Nov | CXM, CXM leadership, ELT viewer, Account executive, VoC admin | Rebuild per the 13 Nov feedback; MVP and Later-phases modes; annotations and traceability for the React build |
| Latest Feedback | 19 Nov | CXM user, CXM leadership, ELT viewer, Sales (AE), Sales leadership, VoC admin | Same screens and logic as Latest; IBM Plex type, PNG logo, Unicode arrows and middots |
| Latest | 19 Nov | same six | NAVEX brand restyle of Latest Feedback (Barlow, NAVEX orange top rule, black primary buttons, pale blue canvas, SVG logo on sign-in and header); glyphs replaced with ASCII. No screen or logic change |
| docs prototype | 19 Nov | same six | Latest plus a bell icon for Notifications and the Notifications nav item hidden |

Note: Latest grew from MVP v1, not from the Handover mockup. It keeps MVP v1 code for screens it no longer links to (see "Unreachable screens").

## Navigation by role and version

| Role | Dec8 / MVP v1 | Handover mockup (MVP mode) | Latest |
|---|---|---|---|
| CXM | Dashboard, Accounts, Verbatim and Comments, Weekly changes, Scheduled digests, Reports, Knowledge hub, Notifications | Accounts | Scorecard, Notifications |
| CXM leadership | Leadership home, Accounts (read only), Manager summary, Custom reports, Knowledge hub, Notifications | Accounts | Scorecard, Manager summary, Custom reports, Notifications |
| ELT viewer | not present | Accounts | none; "Yet to decide the modules and features" |
| Sales (AE) | not present | Accounts (as Account executive) | none; same placeholder |
| Sales leadership | not present | not present | none; same placeholder |
| VoC admin | Admin home, Knowledge hub, Data source health, Role and access, Usage and audit, Notifications | Accounts, Admin (tabs: Refresh and sources, Digests, Usage and audit, Access) | Admin home, Weekly changes, Knowledge hub, Data source health, Usage and audit, Scheduled digests, Notifications |
| Default landing | CXM Dashboard; leadership Leadership home; admin Admin home | Accounts | Scorecard; admin Admin home |

Handover mockup Later-phases mode nav: Phase 1: Product, Phase 1: Knowledge hub, Phase 2: Fact Base (proposals only).

## Latest: what each reachable screen shows

| Screen | Roles | Shows | Spec |
|---|---|---|---|
| Sign-in card | all | Company domain, Sign in with SSO; role field is demo only | AUT-01 |
| Scorecard | CXM, leadership | Refresh notice, AI notice, Red and Yellow cards, ARR at risk by segment cards, week-over-week (leadership only), Filters and search, accounts table with inline detail, Accounts / Saved views tabs | SCR, ACC, SVW, EXP |
| Account detail (inline) | CXM, leadership | Facts, churn score vs VoC sentiment, friction explanation, themes, verbatims (2 per page), friction trend 12 weeks, knowledge hub files linked to the account, Generate account brief (CXM only) | ACC-07 to ACC-13 |
| Manager summary | leadership | This week in brief, team performance with response window | LDR-01 to 03 |
| Custom reports | leadership | Templates with Run; Weekly friction report toggle with filters and Download report | LDR-04, 05 |
| Notifications | all with nav | Role-specific list; leadership also sees emails sent from Weekly changes | ALR-05, 06 |
| Admin home | admin | Excel downloads 7 days, last/next refresh, published files; Next actions; Recent activity | ADM-01 |
| Weekly changes | admin | New red, Repeat red; Email CXM leadership form | ADM-02, 03 |
| Knowledge hub | admin | Upload form (title, file, optional domain), uploads table 5 per page | KHB |
| Data source health | admin | Sources table, Run health check, Refresh runs today | ADM-04, 05 |
| Usage and audit | admin | Highlights, usage rolled up by individual, team, segment, region or a leader's team, audit log | ADM-06 to 08 |
| Scheduled digests | admin | Schedules and Archive tabs, Configure, Preview, Send now, Pause or Resume | DIG-01 to 05 |

## Filters by version (scorecard)

| Filter | MVP v1 | Handover mockup | Latest |
|---|---|---|---|
| Rating | R, Y, G | R, Y, G (Gray to confirm) | R, Y, G |
| Renewal | Renewal quarter, High ARR only | Window 90 / 180 / 365 days | Window: any, within 180 days (T-180), beyond 180 |
| ARR | High ARR only | ARR tier | ARR tier: 50K and above, below 50K |
| Team, CXM | shown to every role; CXM also gets "My accounts only", so a CXM could list all accounts | hidden for CXM | hidden for CXM and AE |
| Other | search, product, theme, segment | search, segment, theme, region, super product family, product issue status, churn language, ARR tier behind "More filters" | search, segment, region, exec sponsor, AE, super product family, theme, issue status, Show new this week |
| Default sort | ARR | ARR highest first | Red with churn language first, then ARR |

## States

| State | Latest | Handover mockup |
|---|---|---|
| Loading | None drawn (static data). The build uses PageLoader, Skeleton, ButtonLoader (Skill notes, front-end skill s6) | None drawn |
| Empty | "No accounts match these filters.", "No themes this period", "No verbatims this period.", "No new red accounts this week.", "No repeat red accounts.", "No new yellow accounts this week.", "No accounts match this template.", "No uploads or drafts yet.", "No knowledge hub files are linked to this account.", saved-views hint | "No accounts match these filters", "No verbatim yet", "No linked product issue", "No change vs last week" |
| Role without modules | Full-page "Yet to decide the modules and features" | n/a (all roles see Accounts) |
| Out-of-scope account | Detail silently falls back to the scorecard | Banner "<account> is outside your access", reason and who to ask |
| Deep link | Not implemented | `#account=<sfdc_id>&src=cta` or `alert`: row expanded, DeepLinkBanner, link back to Gainsight |
| Validation | Hub: title required, file required, type allowed, size cap. Email: 1 to 10 addresses at the allowed domain, no duplicates, subject up to 150 characters | Save view name max 60 |
| Simulated actions | Downloads copy text; toast says download is simulated | Excel export builds a file with metadata rows |
| Notifications | Bell count hidden at zero; opening marks read | n/a |
| Paging | Rows per page 10/25/50; pager hidden at 10 rows or fewer | n/a |

## Unreachable screens still in Latest code

Leadership home, Accounts (read only), Verbatim and Comments, Reports, CXM knowledge hub with drafts, Request a change, CXM users, Role and access, Portfolio heatmap (with High ARR only), Revenue at risk by renewal quarter, Duplicate detection (85% similarity), New upload with validation-approval stages and Google Drive / SharePoint sources. None is in NAV; do not build them from this file. Their text is not current direction.

## Conflicts with docs/

| Topic | Sources say | docs/ says |
|---|---|---|
| Read-only access list | Latest admin nav has no Role and access screen; the Handover mockup has an Access tab | ADM-09 requires it (`docs/01-product/requirements.md`, ADM) |
| Week-over-week chart | Handover md: 8-week trend, `GET /portfolio/trend?weeks=8`, By ARR / By accounts | SCR-07: last week vs this week only, from Latest |
| ELT viewer screens | Latest: placeholder page | LLD 2.1 table gives ELT team filters and an all-accounts chart (`docs/02-architecture/lld.md` 2.1) |
| Leadership knowledge hub | Latest: leadership has no hub | LLD 2.1: leadership uploads and sees own uploads |
| Out-of-scope message | Handover mockup banner says the account is outside your access | AUT-06 and api-contract: identical to not found, 404 |
| Prebuilt digests | Latest: Weekly leadership digest, New red alert, Revenue at risk monthly | DIG-02: Weekly leadership digest, Daily CXM summary, Monthly renewal watch |
| Admin landing | Handover mockup: admin lands on Accounts with an Admin tab | Latest and docs: Admin home; admin has no scorecard nav |
