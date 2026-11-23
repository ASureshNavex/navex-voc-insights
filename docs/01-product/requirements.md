# MVP requirements

This is the build list for the MVP. Each row is one requirement a developer or an AI harness can pick up: what to build, how to tell it is done, who can use it, and where it lives in the repository.

## How to read this file

| Column | Meaning |
|---|---|
| ID | Stable identifier. Use it in branch names, commits, pull requests and tests |
| Requirement | What the user can do or see |
| Done when | Checks a reviewer can run. Every check needs a test or a demo step |
| Roles | Who gets it. Names follow `roles-and-access.md` |
| Web / API | Where the code goes. Paths are relative to `apps/web/src` and `services/experience-api/app` |
| FRD | Matching identifier in FRD v1.0, where one exists |
| Status | `Ready`: build as written. `Confirm`: build to the stated assumption and keep it easy to change; the question is in `open-items.md`. `Hold`: do not build yet |

## Sources and precedence

When sources disagree, the later one wins.

1. Latest prototype, 19 November 2026: `docs/reference/prototype/voc-insights-workspace-latest.html`. It sets screen content, labels, fields and navigation.
2. NAVEX consolidated feedback, 13 November 2026: `docs/reference/navex-mockup-feedback-2026-11-13.md`. It sets the direction: parity first, one view, alerts, SSO, Gainsight linkage.
3. LLD and HLD v0.3: `docs/02-architecture/`. They set data, interfaces and algorithms.
4. FRD v1.0, 11 November 2026: the FRD (`Navex VoC - FRD.docx`, outside this repository). It predates the feedback and is used for identifiers and detail the later sources do not cover.

Product rules that apply to every requirement:

- Parity with the current At-Risk Account Scorecard comes first. No net-new feature is built without NAVEX sign-off.
- The role and persona selectors and the role field on the sign-in card in the prototype exist only to demonstrate roles. The product has neither: identity, role and scope come from SSO.
- Every figure, list and export contains only accounts inside the signed-in user's data scope. The API enforces this; the UI never does it alone.
- Sample accounts, people and figures in the prototype are fictional.

## MVP definition of done

NAVEX stated the MVP is done when these five are true. Every requirement below supports one of them.

| # | Outcome | Requirements |
|---|---|---|
| 1 | Parity with the current report in content, logic and single-view layout | SCR, ACC, EXP, SVW |
| 2 | Stable scheduled refresh | REF, ADM-04, ADM-05 |
| 3 | Change-of-status email alerts | ALR, DIG |
| 4 | SSO-based access | AUT |
| 5 | Gainsight linkage: a CTA opens the account directly, already signed in | AUT-06, ACC-07 |

---

## AUT: sign-in, roles and scope

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| AUT-01 | Sign in through NAVEX Corp AD (Microsoft Entra ID). No local passwords | Opening any route while signed out redirects to Entra and returns to the same route. No password field exists in the app. Tokens are held in memory only, never in `localStorage` or `sessionStorage` | All | `features/auth`, `lib/authConfig.ts` / `core/security.py` | FR-LOG-01, NFR-01 | Ready |
| AUT-02 | Resolve role, permissions and data scope on the server | `GET /api/v1/me/entitlements` returns role, permission list, data scope and scope size. The UI reads permissions from this response only. No component compares role names | All | `features/auth/useEntitlements.ts` / `domains/me`, `core/entitlements.py` | FR-LOG-02, NFR-02 | Ready |
| AUT-03 | A signed-in user with no mapped role sees an access message | API returns `403` with a problem body. The UI shows who to contact and no data. The user stays signed in | All | `components/shared/AccessDenied.tsx` / `core/exceptions.py` | FR-LOG-02 | Ready |
| AUT-04 | Sign out from every page | A Sign out action in the user menu ends the session and returns to the sign-in redirect | All | `components/shared/AppShell.tsx` | FR-LOG-04 | Ready |
| AUT-05 | Record every sign-in for usage reporting | First entitlement call of a session writes an `audit_event` of type `sign_in` with user and time | All | / `domains/me/service.py` | FR-LOG-06 | Ready |
| AUT-06 | Deep link survives sign-in | Opening `/accounts/{sfdc_account_id}?src=cta` or `?src=alert` while signed out lands on that account after sign-in. An account outside scope shows the not-found message, identical to an unknown account | CXM, CXM leadership, VoC admin | `routes/AppRouter.tsx`, `features/accounts` / `domains/accounts` | Feedback: user workflow | Ready |
| AUT-07 | Data scope is bound into every query | Each service function takes `CurrentUser` and applies `scope_filter`. A test proves a CXM cannot read another CXM's account by ID, filter or export | All | / `core/entitlements.py`, every `domains/*/service.py` | NFR-02 | Ready |
| AUT-08 | Session ends after inactivity | Idle period comes from configuration. After it passes, the next action redirects to sign-in | All | `features/auth` | FR-LOG-05 | Confirm: duration from NAVEX IT |
| AUT-09 | No user management screens | The app has no create, edit, deactivate or role-change action. The admin access list is read only | VoC admin | `features/admin` / `domains/admin` | Replaces FR-LOG-03, FR-RAC-03 to 05 | Ready |

## SCR: scorecard, the one view

Route `/accounts`, navigation label "Scorecard". Landing page for CXM and CXM leadership.

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| SCR-01 | Page heading states who and what is in view | Heading "Scorecard". Sub-line gives the user's name, the number of accounts in view and the default sort | CXM, CXM leadership | `features/accounts/ScorecardPage.tsx` / `GET /portfolio/summary` | FR-DSH-06 | Ready |
| SCR-02 | Refresh status notice | Shows the time of the last successful refresh and the next scheduled one, from the published run | CXM, CXM leadership | `features/accounts/RefreshNotice.tsx` / `GET /portfolio/summary` | FR-DSH-01 | Ready |
| SCR-03 | AI notice | A notice states that the report uses AI, reflects the customer's voice, and gives the confidence rating. Text is configuration, not code | CXM, CXM leadership | `features/accounts/AiNotice.tsx` | NFR-04 | Confirm: wording and the source of the confidence figure |
| SCR-04 | Red accounts card | Shows count, ARR in red accounts, a "New red this week" list and a "Repeat red" list. Each list is sorted by ARR, shows account and ARR, and each account opens its row. Empty lists say so | CXM, CXM leadership | `features/accounts/RatingCards.tsx` / `GET /portfolio/summary` | FR-DSH-02, FR-DSH-05 | Ready |
| SCR-05 | Yellow accounts card | Shows count, ARR in yellow accounts and a "New yellow this week" list with the same behaviour as SCR-04 | CXM, CXM leadership | same | FR-DSH-02 | Ready |
| SCR-06 | Total ARR at risk by segment | One card for all segments and one each for Enterprise, MidMarket and SMB. Each shows total ARR at risk, account count, a red and yellow split bar, and red and yellow counts with ARR. Selecting a card sets the segment filter; the selected card is marked | CXM, CXM leadership | `features/accounts/SegmentCards.tsx` / `GET /portfolio/summary` | FR-LHM-03 | Ready |
| SCR-07 | Week over week: red and yellow share | Collapsible section with a one-sentence summary and two charts: share of accounts and share of ARR. Each compares last week with this week as clustered red and yellow bars, with the change in points. Hidden for the CXM role | CXM leadership | `features/accounts/WeekOverWeek.tsx` / `GET /portfolio/trend` | Feedback: landing dashboard | Ready |
| SCR-08 | New and repeat definitions | New red: red this week and not red last week. Repeat red: red both weeks. New yellow: yellow this week and green last week. Computed by the refresh, not the browser | All | / scoring agent `domain/triggers.py`, `tools/serving_store.py` | FR-ACC-02, FR-BKE-04 | Ready |

## ACC: accounts table, filters and detail

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| ACC-01 | Accounts table | Columns in order: Account, ARR, Region and segment, CXM and exec sponsor, Account executive, Next renewal, Rule or trigger, Issue status, NPS, Taxonomy and summary. Server-side filter, sort and paging. Count line reads "x of y accounts" | CXM, CXM leadership | `features/accounts/AccountsTable.tsx` / `GET /accounts` | FR-ACC-01 | Ready |
| ACC-02 | Account cell | Shows name, rating (Red, Yellow, Green in text and colour), New red or Repeat red tag, theme chips, the top verbatim in quotes and the product list | CXM, CXM leadership | same | FR-ACC-02, FR-ACC-03 | Ready |
| ACC-03 | Multiple Enterpret theme chips | An account shows every theme the run ranked for it, straight from the Enterpret taxonomy, with no custom layer. Accounts with none say "No themes this period" | CXM, CXM leadership | `features/themes/ThemeChips.tsx` / `GET /accounts` | FR-ACC-05, Feedback | Ready |
| ACC-04 | Rule or trigger chip | Shows the rule code and text. Codes: AR1 New red this week, AR2 Repeat red, AR4 Churn language, AY1 Green to yellow, AY2 Yellow repeat, AY3 Red to yellow, AG0 no rule matched. Each chip has a tooltip | CXM, CXM leadership | `features/accounts/RuleChip.tsx` / scoring agent `domain/triggers.py` | Parity | Confirm: full rule list from NAVEX rule set |
| ACC-05 | Taxonomy and summary cell | Shows product chips, theme chips, the friction explanation, and a "Churn detail" disclosure with the fired rule and up to three verbatims with source and date | CXM, CXM leadership | `features/accounts/TaxonomyCell.tsx` | Feedback: verbatim next to rating | Ready |
| ACC-06 | Filters and search | One collapsible bar with: Search, Segment, ARR tier ($50K and above, below $50K), Region, Exec sponsor, Account executive, Super product family, Theme, Issue status, Renewal window (within 180 days, beyond), Show (all, new this week), Sort, Rating (Red, Yellow, Green, multi-select). CXM and Team filters appear only with the `scorecard:filter_team` permission. Filters combine, apply at once and only narrow within scope. Clear filters resets them | CXM, CXM leadership | `features/accounts/FilterBar.tsx` / `GET /accounts` query parameters | FR-ACC-04 | Ready |
| ACC-07 | Inline account detail | Selecting a row expands the detail in place, so the user never leaves the one view. A deep link opens the page with that row expanded and highlighted | CXM, CXM leadership | `features/accounts/AccountDetail.tsx` / `GET /accounts/{sfdc_account_id}` | FR-ADT-01, FR-ADT-09 | Ready |
| ACC-08 | Detail facts | CXM, Exec sponsor, Account executive, Region and segment, ARR, Next renewal, Super product family, Product, Issue status, NPS, Previous week, Feedback records | CXM, CXM leadership | same | FR-ADT-01 | Ready |
| ACC-09 | Churn score and VoC sentiment | Shown side by side as two separate measures, each with an (i) tooltip that says what it is and what to do with it. Tooltips open on hover, focus and tap. A note says the two can disagree | CXM, CXM leadership | `features/accounts/MeasuresPanel.tsx` | Feedback: churn score | Confirm: definitions from NAVEX |
| ACC-10 | Friction explanation and themes | One to two sentences generated at refresh, then the theme chips. If generation failed, the panel says the explanation is unavailable and the verbatims still show | CXM, CXM leadership | same / scoring agent `summarise` node | FR-ADT-02 | Ready |
| ACC-11 | Verbatims | Only the records that drive the themes, two per page, with source, date and product. Personal details are masked at ingest. The header shows how many are loaded | CXM, CXM leadership | `features/themes/VerbatimList.tsx` / `GET /accounts/{id}` | FR-ADT-03, NFR-03 | Confirm: masking rules |
| ACC-12 | Friction trend, last 12 weeks | Collapsible bar chart of the friction score, 0 to 100, coloured by band, with a text caption that explains the axes | CXM, CXM leadership | `features/accounts/FrictionTrend.tsx` / `GET /accounts/{id}` | FR-ADT-04 | Confirm: band thresholds |
| ACC-13 | Account brief | "Generate account brief" opens a dialog with the brief: status and previous week, ARR, renewal date, products, friction explanation, supporting feedback and a suggested next step. Copy and Download work. Escape closes it | CXM | `features/accounts/AccountBriefDialog.tsx` / `GET /accounts/{id}/brief` | FR-ADT, Feedback: brief stays | Confirm: whether leadership also gets it |
| ACC-14 | Default sort | Red accounts with churn language first, then other red, then yellow, then green; ARR descending inside each group. Other sorts: ARR highest first, renewal date soonest first | CXM, CXM leadership | / `domains/accounts/service.py` | FR-ACC-06 | Ready |
| ACC-15 | Paging is bounded | `limit` defaults to 50 and is capped at 200. Ordering always ends with the account identifier so pages never repeat or skip rows | All | / `core/pagination.py` | Security skill | Ready |

## SVW: saved views

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| SVW-01 | Save the current filters and sort as a named view | Name is required and unique per user. The view stores filters and sort only, never account data | CXM, CXM leadership | `features/saved-views` / `POST /saved-views` | FR-ACC-08 | Ready |
| SVW-02 | Saved views tab on the scorecard | Tab label shows the count. Each view shows its name and a plain-language summary of its filters | CXM, CXM leadership | `features/saved-views/SavedViewsTab.tsx` / `GET /saved-views` | FR-SVW-01 | Ready |
| SVW-03 | Apply, rename, delete | Apply opens the Accounts tab with the view applied. Rename keeps names unique. Delete asks for confirmation | CXM, CXM leadership | same / `PATCH, DELETE /saved-views/{id}` | FR-SVW-02, 03 | Ready |
| SVW-04 | Private and empty states | A user sees only their own views. With none, the tab explains how to create one | CXM, CXM leadership | same | FR-SVW-04 | Ready |

## EXP: Excel download

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| EXP-01 | Download the filtered scorecard as Excel | The `.xlsx` has the same rows, columns and order as the table under the active filters and scope. The file states the user, time and filters | CXM, CXM leadership | `features/saved-views/exportExcel.ts` / `GET /accounts/export.xlsx` | FR-RPT-03 | Ready |
| EXP-02 | Downloads are audited and counted | Each download writes an `audit_event` with table and row count. The count feeds Admin home and Usage highlights | All with export | / `domains/accounts/service.py` | FR-USG-06 | Ready |
| EXP-03 | Usage and audit tables download too | Usage, grouped usage and audit tables each have Download Excel honouring their filters | VoC admin | `features/admin` / `GET /admin/usage.xlsx`, `GET /admin/audit.xlsx` | FR-USG-05 | Ready |

## ALR: change-of-status alerts and notifications

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| ALR-01 | Email the owner when an account's confirmed status changes | One batched email per owner per alert evaluation run. Subject starts with "Action needed" when the status got worse and "FYI" when it improved. Each account shows previous and new status, top themes, ARR, renewal date and a link | CXM, Account executive | / `services/notifications/src/notifier/alerts.py` | FR-BKE-06, Feedback | Ready |
| ALR-02 | Alerts do not flap | A status must hold for the configured number of runs and clear the dead band before it counts as changed. Covered by unit tests on `confirm_status` | System | / scoring agent `domain/status_confirmation.py` | LLD 5.2 | Confirm: run count, band, cool-down |
| ALR-03 | Alert links open the account | Link format `/accounts/{sfdc_account_id}?src=alert&event={event_id}`. Behaviour as AUT-06 | CXM | `routes/AppRouter.tsx` | Feedback | Ready |
| ALR-04 | Sending is idempotent | A notification row is written before sending. A rerun skips rows already marked sent. Covered by a unit test | System | / `notifier/alerts.py` | LLD 2.3 | Ready |
| ALR-05 | Notifications behind a bell icon | The top bar has a bell icon with an unread count. It opens the notification list for the user's role. Opening the list marks items read. There is no notifications item in the main navigation | CXM, CXM leadership, VoC admin | `features/notifications` / `GET /notifications`, `POST /notifications/read` | FR-KHV-03, FR-LKN-02, FR-SET-03 | Ready |
| ALR-06 | Notification content by role | CXM: weekly insights ready, account moved to red, new red accounts, when the weekly summary goes out. CXM leadership: weekly report ready, new red count, emails sent to them from Weekly changes. VoC admin: refresh scheduled or failed, source failures, knowledge hub upload results | by role | same | same | Ready |

## LDR: CXM leadership

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| LDR-01 | Manager summary, this week in brief | A generated paragraph gives accounts needing attention and their ARR, new red count, the most common friction theme and how many accounts it affects, and the CXM with the most red accounts | CXM leadership | `features/leadership/ManagerSummaryPage.tsx` / `GET /leadership/summary` | FR-MSM-01 | Ready |
| LDR-02 | Team performance highlights | Three tiles: CXM with the most red accounts, CXM with the most ARR at risk, number of overdue responses. A notice lists red accounts past the response window | CXM leadership | same | FR-MSM-03, 04 | Confirm: response data source |
| LDR-03 | Team performance table | One row per CXM in the leader's team: red accounts, responded within the window, overdue, average days to respond, hours spent, high-ARR accounts, high-ARR at red, impacted ARR. A row expands to that CXM's detail | CXM leadership | same | FR-MSM-05, 06 | Confirm: response data source, window (prototype 2 days, FRD 3), high-ARR threshold ($250K) |
| LDR-04 | Custom reports: template list | Lists saved report templates with name, filters and the current number of matching accounts. Run shows account, team, segment, rating and ARR | CXM leadership | `features/leadership/CustomReportsPage.tsx` / `GET /leadership/report-templates`, `POST .../{id}/run` | FR-CRP-02, 03 | Confirm: NAVEX sign-off as beyond parity |
| LDR-05 | Weekly friction report | Filters: product, segment, theme, rating. Columns: account, CXM, segment, product, theme, rating, change versus last week, ARR, renewal date. Download report honours the filters | CXM leadership | same / `GET /leadership/friction-report` | FR-RPT-01 to 03 | Confirm: as LDR-04 |

## ADM: VoC admin

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| ADM-01 | Admin home | Tiles: Excel downloads in the last 7 days, last and next refresh, published knowledge hub files. Panels: next actions with "New upload", and the five most recent audit entries. Landing page for the admin | VoC admin | `features/admin/AdminHomePage.tsx` / `GET /admin/home` | FR-AHM-01 to 03 | Ready |
| ADM-02 | Weekly changes | Two groups against the previous weekly period: New red and Repeat red. Each row shows account, tag, CXM, status change, main theme and ARR, and opens the account. Empty groups say "None this week" | VoC admin | `features/admin/WeeklyChangesPage.tsx` / `GET /admin/weekly-changes` | FR-WCH-01, 02 | Ready |
| ADM-03 | Email CXM leadership from Weekly changes | A form with To, Subject and Message, pre-filled with the week's changes grouped as Action needed and FYI. Validation: 1 to 10 addresses, each valid, at an allowed domain (`navex.com`), no duplicates; subject required, up to 150 characters. Send delivers the email and posts it to leadership notifications. Copy email copies the text | VoC admin | same / `POST /admin/weekly-changes/email` | FR-WCH-03 | Confirm: on hold in LLD pending sign-off |
| ADM-04 | Data source health | Table: source, status (Healthy, Warning, Failed, Not connected), last sync, records, errors, note. Header gives the healthy count. "Run health check" checks all sources on demand | VoC admin | `features/admin/SourceHealthPage.tsx` / `GET /admin/source-health`, `POST /admin/source-health/check` | FR-SRC-01, 04 | Ready |
| ADM-05 | Refresh runs | Table: time, status (Success, Failed, Scheduled), accounts processed, note. States that call transcripts are not used for scoring in the MVP | VoC admin | same / `GET /admin/refresh-runs` | FR-SRC-03 | Ready |
| ADM-06 | Usage highlights | Tiles: most views in 7 days, top CXM by views, active users in 7 days, Excel downloads in 7 days, average views per user | VoC admin | `features/admin/UsageAuditPage.tsx` / `GET /admin/usage/highlights` | FR-USG-01 | Ready |
| ADM-07 | Usage along the org chart | Roll up by individual, team, segment or region, or by a leader's team. Individual columns: user, role, team, segment, region, last login, views in 7 days, active weeks of 4, returned this week. Group columns: users, views, average views, active, returned. Search, column filters and a date range | VoC admin | same / `GET /admin/usage?group_by=` | FR-USG-02, 04, 05 | Ready |
| ADM-08 | Audit log | Time, who, action, newest first. Filter by who and date range; rolls up with the usage dimension | VoC admin | same / `GET /admin/audit` | FR-USG-06, NFR-10 | Ready |
| ADM-09 | Read-only access list | Shows what each role can see and each user's role and accounts in scope, all from SSO and the org chart | VoC admin | `features/admin/AccessPage.tsx` / `GET /admin/access` | FR-RAC-01, 02 | Ready |

## DIG: scheduled digests

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| DIG-01 | Digest schedules | Table: digest, audience, schedule, next run, archive period, status (Active, Paused), with Preview, Configure and Pause or Resume | VoC admin | `features/digests/DigestsPage.tsx` / `GET /admin/digests` | FR-DIG-01, 07 | Ready |
| DIG-02 | Prebuilt digests | Weekly leadership digest (CXM leadership, their team), Daily CXM summary (each CXM, own accounts), Monthly renewal watch | VoC admin | / seed data in `packages/voc-data` | FR-DIG-02 | Ready |
| DIG-03 | Configure | Schedule: daily, weekdays, weekly on Monday, monthly on the 1st, at a set time. Content: red accounts, yellow accounts, new red this week, overdue red responses, renewals in the next 90 days | VoC admin | same / `PATCH /admin/digests/{id}` | FR-DIG-03, 04 | Confirm: "overdue red responses" depends on LDR-02 |
| DIG-04 | Preview and send now | Preview shows the digest as a recipient sees it. Send now queues it for the notification task | VoC admin | same / `POST /admin/digests/{id}/preview`, `/send` | FR-DIG-06 | Ready |
| DIG-05 | Archive | Sent digests are kept 30 days: digest, sent time, archive date, accounts needing attention | VoC admin | same / `GET /admin/digests/archive` | FR-DIG-08 | Ready |
| DIG-06 | Every digest states whether action is needed | Subject and first line say "Action needed" or "FYI". A CXM with no red or yellow accounts gets no CXM digest | Recipients | / `notifier/digests.py` | FR-DIG-05, Feedback | Ready |
| DIG-07 | Light personal digest settings | A user can turn their own digest on or off and choose its frequency from the admin's options | CXM, CXM leadership | `features/digests/DigestPreferences.tsx` / `GET, PUT /me/digest-preferences` | Feedback | Confirm: not in the latest prototype |

## KHB: knowledge hub

| ID | Requirement | Done when | Roles | Web / API | FRD | Status |
|---|---|---|---|---|---|---|
| KHB-01 | Upload to the knowledge hub | Form: title (required), file (required), domain (optional). The browser gets a presigned URL and sends the file straight to S3; the API never receives file bytes | VoC admin | `features/knowledge-hub/UploadForm.tsx` / `POST /knowledge-hub/uploads`, `POST /knowledge-hub/files/{id}/complete` | FR-KHM-01 | Ready |
| KHB-02 | File checks | Allowed types: PDF, DOCX, CSV, XLSX, PPTX. Maximum 25 MB. No duplicate of a published file. A failed check rejects the file with the reason. Type is verified from the file signature, not the name; files are malware scanned before they are readable | VoC admin | same / `domains/knowledge_hub/service.py`, `ports/document_store.py` | FR-KHM-02, 03, NFR-15 | Confirm: limits |
| KHB-03 | Uploads list | Table: upload (title, file name, ID), domain, size, uploaded by, status (Draft, Published), five per page with paging | VoC admin | `features/knowledge-hub/UploadsTable.tsx` / `GET /knowledge-hub/files` | FR-KHM-04 | Ready |
| KHB-04 | Publication rule | Latest prototype: a file that passes checks is published straight away. LLD v0.3: CXM leadership uploads and a VoC admin approves or declines with a reason. The status model supports both; the approval step is switched by configuration | VoC admin; CXM leadership if confirmed | / `domains/knowledge_hub/status.py` | FR-KHM-05, 06, FR-LKN-01 | Confirm: which rule applies in the MVP |
| KHB-05 | Audit | Uploads, check results and decisions are written to the audit log | System | / `domains/knowledge_hub/service.py` | FR-KHM-07 | Ready |
| KHB-06 | Not in the CXM view | The CXM role has no knowledge hub navigation, route or API access | CXM | `routes/navigation.ts` / permission guard | Feedback | Ready |

## REF: ingestion and account scoring

The background work is two units. The ingestion task (`services/ingestion`, ECS Fargate) does the deterministic preparation: pull, match, mask, stage. The Account Scoring Agent (`services/account-scoring-agent`, LangGraph on AgentCore Runtime) scores, explains and publishes. Together they productionise the scorecard skills NAVEX runs by hand today. Only the written summaries use a model.

| ID | Requirement | Done when | Roles | Where | FRD | Status |
|---|---|---|---|---|---|---|
| REF-01 | Scheduled refresh | EventBridge Scheduler starts the ingestion task on the agreed schedule. A run does not start while another is active | System | ingestion `pipeline.py`, `adapters/staging.py` | FR-BKE-01 | Confirm: frequency. Prototype shows two times in one place and "once a day" in another; FRD says three |
| REF-02 | Pull accounts and feedback | Account master from Snowflake; taxonomy, theme and sentiment counts and driver verbatims from Enterpret through its MCP API. Code calls the tools directly; no model chooses them | System | ingestion `adapters/snowflake.py`, `adapters/enterpret.py` | FR-BKE-01 | Confirm: field mapping |
| REF-03 | Match, mask and stage | Feedback is matched to accounts on the Salesforce account ID. Unmatched records are counted and reported in source health. Personal details are masked before a verbatim is stored. Evidence is staged per run | System | ingestion `matching.py`, `masking.py`, `adapters/staging.py` | FR-SRC-02, NFR-03 | Confirm: masking rules |
| REF-04 | Hand over to the agent | When staging succeeds the task starts the Account Scoring Agent with the run ID. A source failure fails the run, starts nothing and leaves the published run in place | System | ingestion `adapters/agentcore.py` | NFR-06 | Ready |
| REF-05 | Score with NAVEX's versioned rule set | Rating, rule or trigger and confidence come from code. Every rating records its rule set version. The same inputs always give the same rating | System | agent `domain/scoring.py`, `domain/triggers.py`, `rules/` | FR-BKE-02, NFR-16 | Confirm: rule set import from NAVEX |
| REF-06 | Rank themes and pick driver verbatims | Themes ranked by negative volume, then total volume. For the top three themes keep the most recent verbatims up to a fixed count | System | agent `domain/theme_ranking.py` | LLD 5.4, 5.5 | Confirm: negative or total volume leads |
| REF-07 | Written summaries | Friction explanation per red or yellow account from a Jinja2 prompt with Pydantic structured output. Verbatims are passed as delimited data. Every cited ID must be in the evidence. Unchanged evidence reuses the previous text. A failed summary never blocks the rating | System | agent `prompts/account_scoring/`, `graphs/account_scoring/nodes.py` | FR-BKE-03, NFR-04 | Ready |
| REF-08 | Publish atomically | Results are written per run and become visible only when `published_run` switches in one transaction. A failed run leaves the last good run in place | System | agent `tools/serving_store.py` | NFR-06 | Ready |
| REF-09 | Weekly comparison | Each run writes the week's snapshot. New red, repeat red and new yellow compare with the previous week's snapshot | System | agent `tools/serving_store.py`, `domain/triggers.py` | FR-BKE-04 | Confirm: weekly cut-off day and time |
| REF-10 | Emit `run.published` | The event carries the run ID and the number of status changes. A failed run or source notifies VoC admins | System | agent `tools/events.py` | FR-SRC-05 | Ready |

## NFR: quality requirements

| ID | Requirement | Done when | FRD | Status |
|---|---|---|---|---|
| NFR-A | Security review passes | No finding at Blocker level from `.harness-records/skills/navex-security-code-review` | NFR-01 to 04 | Ready |
| NFR-B | Accessibility | WCAG 2.1 AA: visible focus, labelled controls, rating in text as well as colour, keyboard access to tooltips and dialogs, reduced motion respected | NFR-12 | Ready |
| NFR-C | Responsive | Works from 390px wide. Below 1024px the accounts table becomes cards with the same fields | NFR-11 | Ready |
| NFR-D | Performance | Scorecard first load and filter changes respond within 3 seconds for a typical scope | NFR-07 | Confirm: target |
| NFR-E | Browser support | Current Microsoft Edge and Google Chrome | NFR-13 | Ready |
| NFR-F | Observability | API, agent and notification task emit OpenTelemetry traces, metrics and JSON logs. No token, secret or verbatim text is logged | NFR-10 | Ready |
| NFR-G | Copy quality | Every label and message passes a grammar review; wording matches the latest prototype | Feedback | Ready |
| NFR-H | Quality gate | `ruff`, `mypy --strict`, `pytest`, `pip-audit`, `tsc --noEmit`, `eslint`, `vitest` and `trivy` pass in CI | Skills | Ready |

## Removed from the MVP

Do not build these. They appear in the FRD or an earlier mock-up and NAVEX removed them.

| Item | FRD | Reason |
|---|---|---|
| Meetings in the next 20 days; next meeting fields | FR-DSH-02, FR-ACC-01 | Not requested or validated |
| Next renewal date tile | FR-DSH-02 | The date stays on each account |
| High ARR only filter | FR-ACC-04, FR-SET-02 | Sort by ARR covers it |
| Renewal quarter column | FR-ACC-01 | Rule-based renewal window filter instead |
| CXM commentary and "My feedback" | FR-ADT-05 to 08, FR-BKE-05 | CXMs log this in Salesforce and Gainsight |
| Manual user management | FR-LOG-03, FR-RAC-03 to 05 | SSO handles it |
| Knowledge hub in the CXM view | FR-KHV-01, 02 | As requested |
| Separate dashboard, verbatim search and report pages for the CXM | FR-VRB, FR-RPT, FR-WCH for CXM | Merged into the one view |
| Nine-week trend line | FR-DSH-03 | Replaced by SCR-07 |

## Later phases

Not MVP scope. Keep the data model open to them. Detail is in `docs/reference/phase-scope-workbook.md`.

- Product workspace: domain friction table, domain deep dive, topic research
- Fact Base with enterprise views
- A simple action that creates a CTA or issue in Gainsight or Salesforce, with write-back
- VoC rating fed into the T-180 renewal brief
- Approved knowledge hub files used as evidence
- Modules for ELT, Sales (AE) and Sales leadership, which the latest prototype marks as "Yet to decide the modules and features"
