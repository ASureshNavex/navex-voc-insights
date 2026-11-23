# 02 Functional requirements: FRD residue and conflicts
Sources: Navex VoC - FRD.docx (v1.0, 11 Nov 2026) sections 1.3-9; NAVEX VoC - Discovery Closure Document.pptx slide 9.

The FRD is already in `docs/` word for word, and the MVP build list maps its ids. This file holds only what the FRD has that the build list does not carry, plus where they disagree.

## Already in docs/ (read there, not here)

- Full FRD text, every FR-xxx-nn and NFR-nn id with its description: the FRD (`Navex VoC - FRD.docx`, outside this repository) "5 Functional Requirements" (5.1 to 5.5) and "Non-Functional Requirements".
- MVP build list, with the matching FRD id in its `FRD` column and a status of Ready, Confirm or Hold: `docs/01-product/requirements.md` (identical copy: `docs/01-product/requirements.md`). Source precedence: "Sources and precedence" there. The later prototype and NAVEX feedback win over the FRD.
- FRD items NAVEX removed from the MVP: `docs/01-product/requirements.md` "Removed from the MVP".
- FRD vs design baseline: `docs/02-architecture/hld.md` "2. Scope baseline after customer feedback".
- FRD permission matrix: the FRD (`Navex VoC - FRD.docx`, outside this repository) "4.2 Permission Mapping"; current matrix: `docs/01-product/roles-and-access.md` "Permissions".
- FRD assumptions, risks, dependencies: the FRD (`Navex VoC - FRD.docx`, outside this repository) "Assumptions", "Risks", "Dependencies and Open Points".

## FRD requirements with no home in the MVP build list

These are not mapped in `docs/01-product/requirements.md` and not in its "Removed" table. Status is Open unless noted. Decide each one: carry it over, or add it to "Removed".

| FRD id | Requirement (one line) | FRD acceptance detail |
|---|---|---|
| FR-DSH-04 | Accounts needing attention list | Red before yellow, highest ARR first; shows main theme, rating, New red tag, ARR, renewal date |
| FR-ACC-07 | High ARR flag on accounts | ARR at or above an admin-set threshold; proposed $250K (Open, FRD dep 7) |
| FR-LHM-01 | Leadership revenue at risk | ARR of red and yellow accounts grouped by renewal quarter, with total |
| FR-LHM-02 | Leadership portfolio summary | Red count, yellow count, impacted ARR, new red this week |
| FR-LHM-04 | Leadership view marked read only | Page states the view is read only |
| FR-LAC-01/02 | Leadership account list and detail across all accounts | As FR-ACC, FR-SVW, FR-ADT, without adding feedback |
| FR-MSM-02, FR-SET-01 | Response window setting | Admin sets days for a CXM to respond to a red account; default 3 (Open, FRD dep 6); applies from next refresh; changes logged |
| FR-SET-02 | High ARR threshold setting | Admin edits the threshold; NFR-16 requires it configurable without code change |
| FR-CRP-01 | Create a custom report template | Save weekly friction report filters, across all accounts, as a named template |
| FR-CRP-04 | Edit and delete a custom report template | - |
| FR-USG-03 | Red account responses by product | Per product: red accounts responded to; CXM with most responses |
| FR-SRC-01 (part) | Named MVP sources on the source health page | Enterpret feedback records; Snowflake account metadata; support case data |
| FR-DIG-03 (part) | All digests of one run are sent at the same time | - |
| NFR-05 | Data freshness caveat | Source data may arrive up to three business days after submission; last refresh time shown |
| NFR-09 | Scalability | Supports all MVP users and accounts, and Phase 1's added users without redesign |
| NFR-17 | Maintainability and handover | Documented and handed over so a NAVEX engineer can run and change it |

## FRD dependencies mapped to docs/ open items

FRD list: the FRD (`Navex VoC - FRD.docx`, outside this repository) "Dependencies and Open Points". docs list: `docs/01-product/open-items.md`.

| FRD dep # | Item | Owner (FRD) | docs/ open item |
|---|---|---|---|
| 1 | SSO and employee group contact | NAVEX | #12 |
| 2 | Snowflake access | NAVEX | None (#10 covers field mapping only) |
| 3 | Enterpret access, incl. taxonomy for filters (In progress) | NAVEX | #18 (in part) |
| 4 | Example of the current weekly email, for digest content | NAVEX VoC team | None |
| 5 | Knowledge hub upload for CXM users and leadership | NAVEX | #1 |
| 6 | Default response window | CXM leadership | #3 |
| 7 | High ARR threshold | NAVEX VoC team | None |
| 8 | Allowed knowledge hub file types, incl. Teams recordings | NAVEX VoC team | None (KHB-02 "Confirm: limits") |
| 9 | Download format; verbatim masking rules | NAVEX | Format settled as Excel (`hld.md` section 2); masking #16 |
| 10 | Handling of Gray ratings | NAVEX VoC team | #9 |
| 11 | Gainsight target for CXM feedback (Phase 1) | Gainsight admin | None (later phase) |
| 12 | Baselines for the value framework | NAVEX VoC team | None |
| 13 | Consolidated CXM navigation layout | Psiog | #14; one view settles the layout |

FRD risks with no docs/ counterpart (FRD "Risks"): access delays to Snowflake, Enterpret or SSO, tracked through an access checklist; a scoring model change mid-build (for example call transcripts), mitigated by a fixed MVP baseline and versioned, tested changes; scope additions, which go through change control or move to Phase 1; Enterpret usage or licence limits, to be confirmed before build.

## Conflicts with docs/

Not repeated here: the removals that docs/ already acknowledges (commentary, user management, meetings, High ARR filter, renewal quarter, separate CXM pages, nine-week trend). See `docs/01-product/requirements.md` "Removed from the MVP".

| Topic | FRD / source | docs/ |
|---|---|---|
| Account brief | Out of scope; Phase 1 (FRD 1.3.2) | In MVP for the CXM (`requirements.md` ACC-13). Closure slide 9 also has it in the MVP |
| Knowledge hub upload fields | Title, file and account are required; domain is optional; source type is interview notes, CAB notes, competitive intelligence or other (FR-KHM-01) | Title, file and domain (optional); no account, no source type (KHB-01) |
| Knowledge hub duplicates | Blocked for the same file against the same account, allowed against a different account; the uploader is told who uploaded it and when (FR-KHM-03) | "No duplicate of a published file" (KHB-02) |
| Knowledge hub statuses | Draft, Validation, Awaiting approval, Published, Declined (FR-KHM-05) | Draft, Published in the list (KHB-03); approval switched by configuration (KHB-04, open item #1) |
| Admin home tiles | Uploads awaiting approval, last and next refresh, published files (FR-AHM-01) | Excel downloads in 7 days replaces uploads awaiting approval (ADM-01) |
| Weekly changes | CXM page; four groups: New red, Repeat red, Improved, Worsened (FR-WCH-01); the CXM emails their leadership (FR-WCH-03) | VoC admin page; two groups, New red and Repeat red (ADM-02); the admin sends the email (ADM-03) |
| Weekly digest day | Weekly on a chosen day (FR-DIG-03) | Weekly on Monday (DIG-03) |
| Default digest names | Leadership digest, CXM digest, monthly renewal watch (FR-DIG-02) | Weekly leadership digest, Daily CXM summary, Monthly renewal watch (DIG-02) |
| Leadership landing page | Leadership home with revenue at risk by renewal quarter (FR-LHM-01 to 04) | Leadership lands on the Scorecard; only the team table carries over, as segment cards (SCR-06 maps FR-LHM-03) |
| Attention ordering | Red before yellow, then ARR descending (FR-DSH-04) | Red with churn language first, then other red, yellow, green, then ARR (ACC-14) |
| High ARR threshold | Admin setting, $250K proposed (FR-ACC-07, FR-SET-02, NFR-16) | No setting; LDR-03 still uses "high-ARR ($250K)"; ARR tier filter at $50K (ACC-06) |
| Response window setting | Admin-editable, default 3 days (FR-SET-01) | No setting requirement; window value open, 2 or 3 days (LDR-03, open item #3) |
| Email service | NAVEX-approved email service (NFR-14) | SES behind a Mailer port (open item #15) |
| Refresh frequency | Three times a day (FR-BKE-01, NFR-05) | Open (REF-01, open item #2). Closure slide 9: daily, with three a day subject to cost and limits |

## Open questions

- FRD 1.4 cites a "Report inventory and value framework" (metrics, baselines, targets). It is not in `docs/` beyond that citation, and not in this slice.
- Should each item in "FRD requirements with no home" be built or recorded as removed? NAVEX has not said.
