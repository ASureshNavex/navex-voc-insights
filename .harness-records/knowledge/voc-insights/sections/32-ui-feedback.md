# UI feedback and its status

Sources: Feedback 13 Nov (`docs/reference/navex-mockup-feedback-2026-11-13.md`, same text as the zip copy), Navex_Notes_15_OCT_2026.txt (Notes 15 Oct, Lnnn), Navex_VoC_Meeting_Transcript.txt (Transcript), Response to technical questions 13 Nov (Tech answers), Artifacts/NAVEX_VoC_Mockup_React_Handover.md (Handover md), Handover mockup traceability table (16 Nov), Latest prototype 19 Nov (Latest).

Status is judged against the Latest prototype, the screen reference per `docs/01-product/requirements.md`, "Sources and precedence". done = Latest shows it as asked. open = not in Latest, or waiting on NAVEX. Item text is a short label; read the feedback file for the wording.

## A. NAVEX consolidated feedback, 13 Nov (on MVP v1)

Section names follow `docs/reference/navex-mockup-feedback-2026-11-13.md`.

| # | Item (section) | Status | Evidence |
|---|---|---|---|
| A1 | Parity first, one view (Overall direction) | done | Scorecard holds cards, table, themes, verbatim and inline detail |
| A2 | No net-new features without sign-off (Overall direction) | open | Latest still adds Manager summary response tracking and Custom reports; see `docs/01-product/open-items.md` #3, #5 |
| A3 | Keep Red and Yellow counts and impacted ARR (Landing) | done | Red and Yellow cards |
| A4 | Split impacted ARR into Red ARR and Yellow ARR (Landing) | done | ARR per card |
| A5 | New Red and New Yellow this week replace "What's new" (Landing) | done | Lists inside the cards |
| A6 | Remove Next renewal date tile (Landing) | done | Not shown |
| A7 | Remove Meetings in 20 days (Landing) | open | Removed from scorecard, but the account brief still prints a next meeting line; open item #6 |
| A8 | Week-over-week clustered bar by volume and ARR (Landing) | done | Leadership only; last week vs this week |
| A9 | Copy and grammar pass (Landing) | open | Waiting on NAVEX review (Handover md s6) |
| A10 | Keep R/Y/G filter (Accounts) | done | Rating checkboxes |
| A11 | Remove High ARR only (Accounts) | done | Replaced by ARR tier; survives only in unreachable heatmap code |
| A12 | Multiple Enterpret theme chips (Accounts) | done | Chips per account; report columns still use the first theme |
| A13 | Themes straight from the Enterpret taxonomy (Accounts) | done | Note in account detail |
| A14 | Verbatim back in the main table (Accounts) | done | Top verbatim in the account cell; Churn detail disclosure |
| A15 | One next-renewal date, no Renewal quarter column, rule-based window (Accounts) | done | Next renewal column; Renewal window filter |
| A16 | Product at account level (Accounts) | done | Product line in the account cell |
| A17 | Excel download of filtered table (Accounts) | done | Download Excel (simulated) |
| A18 | Detail carries the fuller set (Account detail) | done | Inline detail |
| A19 | Trim supporting feedback to theme drivers (Account detail) | done | Two verbatims per page; masking open item #16 |
| A20 | Remove CXM commentary (Account detail) | open | Gone from screens, but response tracking built on it remains in Manager summary; open item #3 |
| A21 | Account brief as is (Account detail) | done | CXM only; leadership access open item #6 |
| A22 | Access and hierarchy from SSO and org chart, no user management (Roles) | done | No user screens; read-only access list not reachable in Latest |
| A23 | CXM sees own accounts; no Team or CXM filters for CXM (Roles) | done | Filters hidden for CXM and AE |
| A24 | ELT all-access viewer; Sales by ownership (Roles) | open | Roles exist, modules "Yet to decide"; open item #4 |
| A25 | Full set of access levels incl. Product (Roles) | open | NAVEX to confirm |
| A26 | Usage and audit along org chart; drop non-engagement panels (Roles) | done | Roll up by individual, team, segment, region, leader's team |
| A27 | Change-of-status email and VoC CTA in Gainsight (Workflow) | open | Not in Latest; previewed in the Handover mockup only. CTA built by NAVEX |
| A28 | Open the account from alert or CTA, signed in (Workflow) | open | No deep link in Latest; Handover mockup has it; AUT-06 specifies it |
| A29 | Gainsight home-page entry point (Workflow) | open | Gainsight admin question (Tech answers Q4) |
| A30 | Every alert and digest says Action needed or FYI (Workflow) | done | Weekly changes email sections and subject |
| A31 | Anything that matters downstream writes back, no duplicate entry (Workflow) | open | Write-back is Phase 1 (Tech answers Q5) |
| A32 | Admin-level prebuilt digests (Workflow) | done | Scheduled digests |
| A33 | Light personal digest settings for CXMs (Workflow) | open | In Handover mockup profile menu, absent from Latest; open item #7 |
| A34 | Churn score beside VoC sentiment, (i) tooltips (Workflow) | done | Definitions open item #8 |
| A35 | Later: checkbox to create CTA or issue, T-180 routing, TechTorch brief (Workflow) | open | Later phase; Handover mockup proposal |
| A36 | Saved views, keep (Added features) | done | Saved views tab |
| A37 | Refresh three times daily pending cost (Added features) | open | Cost answered (10 to 25 USD a month, Tech answers Q1); Latest shows 12:00/18:00 and "once a day"; open item #2 |
| A38 | Knowledge hub out of the CXM view (Added features) | done | Admin only |

## B. Feedback from discovery, not in the feedback file

| # | Item | Status | Source |
|---|---|---|---|
| B1 | One self-serve source, regularly updated, replacing an HTML report on a SharePoint page | done (design) | Transcript 1:20-1:38; Notes 15 Oct L411 |
| B2 | Role-based access, absent in the current report | done (design) | Transcript 1:20 |
| B3 | Show accounts on the red list last week vs this week | done | Weekly changes, week-over-week; Notes 15 Oct L398 |
| B4 | Daily view of today | open | Refresh frequency undecided; Notes 15 Oct L399 |
| B5 | Track adoption: who uses the solution | done | Usage and audit; Notes 15 Oct L405-408 |
| B6 | CXM leadership filters their team or account views | done | Team and CXM filters for leadership; Notes 15 Oct L416 |
| B7 | Flag repeats vs first-time red; rank by ARR; filter by next renewal date | done | New red / Repeat red tags, ARR sort, renewal window; Notes 15 Oct L433-435 |
| B8 | Escalate high-risk accounts using churn language for leadership attention | done | AR4 churn-language rule sorts first; Notes 15 Oct L429-430 |
| B9 | VoC score and Gainsight score side by side without confusing the CXM | open | Two-measure card shown; definitions pending; Notes 15 Oct L447 |
| B10 | Admin library to upload call recordings, CSV, PDF, Word, Teams recordings, Excel | open | Latest allows pdf, docx, csv, xlsx, pptx only; no recordings; Notes 15 Oct L382-386 |
| B11 | Show Impacted ARR, number of accounts at risk, next renewal date | done | Cards and renewal column (renewal tile later removed); Notes 15 Oct L536 |
| B12 | Show the data gap: next meeting date per account | open | Meetings removed per Feedback 13 Nov; Notes 15 Oct L537 |
| B13 | Primary theme rule: highest negative volume vs highest volume | open | Tech answers Q6; `docs/02-architecture/lld.md` 5.4 |

## C. Items the Handover md lists as waiting on NAVEX (16 Nov)

Copy and grammar review; Gray as a fourth rating; full parity field list; churn score and VoC tooltip definitions; full access levels (Product, Sales leadership); Gainsight home-page entry point; refresh frequency against cost. All open; each is tracked in `docs/01-product/open-items.md` (#8, #9, #10, #4, #2) except the copy review and the Gainsight entry point.

## D. Changes made on 19 Nov with no written feedback in the sources

Between the Handover mockup (16 Nov) and Latest (19 Nov) the direction moved: admin pages split out of the Admin tab, knowledge hub returned for admins, leadership pages (Manager summary, Custom reports) returned, ELT and Sales got placeholder pages, default sort became churn-language first, renewal window became T-180. The file name "Latest Feedback" implies a review, but no feedback text for it is in the sources. Treat these as unconfirmed.

## Conflicts with docs/

| Topic | Sources say | docs/ says |
|---|---|---|
| Copy review and Gainsight home-page entry point | Waiting on NAVEX (Handover md s6) | Not listed in `docs/01-product/open-items.md`; NFR-G marks copy quality Ready |
| Upload formats | Notes 15 Oct asks for call recordings and Teams recordings as well as documents | KHB-02 allows PDF, DOCX, CSV, XLSX, PPTX only, with no open item on media files |
