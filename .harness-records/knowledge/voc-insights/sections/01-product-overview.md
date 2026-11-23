# 01 Product overview: discovery context
Sources: Navex VoC - FRD.docx (v1.0, 11 Nov 2026) sections 1-3; NAVEX VoC - Discovery Closure Document.pptx (Nov 2026) slides 2-11; NAVEX_VoC_Solution_Proposal.pptx (Oct 2026) slides 2-4.

This file complements `docs/`; it does not restate it. Read the pointers first.

## Already in docs/ (read there, not here)

- What the application is, problem table, users, expected flow, data sources, phases, MVP definition of done, product rules: `docs/01-product/overview.md` (all headings).
- Roles, data scopes and permissions: `docs/01-product/roles-and-access.md` "Roles", "Data scopes", "Permissions".
- Terms: `docs/01-product/glossary.md`.
- FRD project overview, as-is challenges, to-be "what changes": the FRD (`Navex VoC - FRD.docx`, outside this repository) "1.1 Project Overview", "2.3 Challenges", "3.3 What changes".
- MVP scope baseline after NAVEX feedback (FRD vs design): `docs/02-architecture/hld.md` "2. Scope baseline after customer feedback".

## Business decisions the insight serves (Closure slide 3)

| | Customer Success | Product |
|---|---|---|
| Decision | Which accounts need intervention before renewal, and why | What to fix or build next, and the evidence for it |
| Owner | CXMs, supported by CXM leadership | Product managers, one per product domain |
| Measured on | Retention and ARR at renewal; renewal workflows start 180 days out | Domain roadmap and strategy, reviewed quarterly |
| Signal used | Account friction rating plus themes and verbatims | Domain friction rating, thematic roll-ups, monthly Fact Base |
| Where work happens | Gainsight, Salesforce | Aha! |

Context that shapes the solution (Closure slide 3):
- AI thematic roll-ups have existed for under a year; trust is still forming, so the reason behind every rating must stay visible.
- Support cases are over 80% of feedback. Call transcripts were entering Enterpret in Nov 2026 and may change the scoring model.
- No single function owns VoC across NAVEX, so the platform must make usage and follow-through visible rather than assume them.

## As-is capability chain (Closure slide 4)

| Step | State | What exists |
|---|---|---|
| Capture | In place | Support cases, product ideas, NPS, CSAT into Snowflake via BI-team integrations |
| Classify | In place | Enterpret: three-level taxonomy, feedback type, sentiment, written back to Snowflake |
| Score | In place | Account and domain friction models rate accounts and product domains Red/Yellow/Green |
| Distribute | Manual | Weekly At-Risk Account Scorecard and monthly product reports by email and SharePoint |

Loop status: Detect and Explain in place; Deliver manual; Act and Measure not connected. Closing that loop is the platform's job (Closure slide 4).

## Systems landscape (Closure slide 5)

Only rows `docs/01-product/overview.md` "Data sources" lacks:

| System | Role today |
|---|---|
| Enterpret | Restricted to the VoC team because it has no audit trail; analysis requests route through the VoC team |
| Aha! | Ideas, votes, initiatives, product fact bases (Product's tool) |
| Claude skills + SharePoint | Today's manual reporting layer: six skills, about 13 files, one HTML report, produced weekly by one person |
| Power BI | Existing analytical dashboards; continues alongside the platform (Proposal slide 3) |

Implication (Decided, Closure slide 5): Snowflake and Enterpret stay as they are; the platform replaces the manual reporting layer, not the data core.

## Problem behind the ask (Closure slide 6)

- Stated need: insight reaches owners late, untargeted, through two people, with little visibility of follow-through.
- Required state: each owner is alerted on a status change, understands why, acts in Gainsight; usage visible to leadership.
- Root causes: production (six skills, ~13 files weekly); distribution (one file, forwarded by leaders); follow-through (no trigger, no signal-to-action link); governance (no Enterpret audit trail, usage only as page views); trust (explanations hand-corrected before release).
- Why now: red accounts carry ARR into renewal; leadership wants a dependable at-risk view for the 8 December 2026 board meeting.
- Fix covers production, distribution and governance fully; follow-through only by making action visible.

Stays a NAVEX decision, outside the platform (Decided, Closure slide 6):
- Acting on an at-risk account is a Customer Success decision taken in Gainsight.
- Product teams are not required to respond to VoC insight (executive decision).
- Ownership of VoC across NAVEX is an operating-model choice.

## Capability path by phase (Closure slide 7)

See, Explain, Alert, Act, Measure; each phase extends one governed platform to a new audience. Phase detail: `03-scope-phase-1-and-target.md`.

## What NAVEX validates at MVP, and expected value (Closure slide 10)

| Validated | Expected value |
|---|---|
| Scorecard parity in one view: ratings, Enterpret themes, verbatims together | CXMs see why an account is flagged without moving across pages |
| Stable daily refresh; status-change email says action needed or FYI | Owners know what changed and whether it needs attention |
| SSO and role-based visibility by role and ownership | No separate permission set to maintain |
| Gainsight CTA opens the account in the workspace; follow-up in Gainsight | CXMs review evidence then return to their workflow |

Post-rollout measures (Closure slide 10): refresh and alert reliability, workspace engagement, effort to produce and distribute the scorecard. Proposal exit criterion for MVP: "Live, used by CXMs, no manual effort" (Proposal slide 4).

## Discovery closure: confirmations requested (Closure slide 11)

| Item | What to confirm | Led by |
|---|---|---|
| MVP business scope and prototype | Scorecard experience, included capabilities, agreed exclusions | NAVEX VoC lead and CSO |
| MVP technical solution | Architecture direction; conditions on data access, refresh, identity, Gainsight | NAVEX technical lead |
| Delivery handoff | Owner and next step per open dependency; Phase 1 and Target State as roadmap | NAVEX and Psiog |

Discovery method (Closure slide 2): two weeks, six stakeholder sessions (VoC lead, CSO organisation, data and technical leads), process walk-through, artefact review, prototype validation with the VoC lead and CSO.

## Conflicts with docs/

| Topic | docs/ says | Source says |
|---|---|---|
| Later phase names and dates | Phase 1 9 Dec 2026 - 15 Feb 2027; "Phase 2" 16 Feb - 30 Mar 2027 (`docs/01-product/overview.md` "Phases") | Milestone 2 / Phase 1 Jan - Feb 2027; Milestone 3 / "Target State" from Mar 2027, open-ended (Proposal slide 4); FRD and Closure use "Target State", never "Phase 2" (FRD 1.3; Closure slide 7) |
| Hosting and AI runtime | AWS; Account Scoring Agent on Amazon Bedrock AgentCore (`docs/02-architecture/overview.md` table row "Account Scoring Agent") | Recommended: React app with Snowflake backend, Cortex AI, hosted on Snowpark Container Services, NAVEX-approved cloud as alternative (Proposal slide 3). "AI boundary (Cortex or Claude direct)" listed as a Milestone 1 decision (Proposal slide 4) |
| Snowflake direction | Snowflake read only (`docs/01-product/overview.md` "Data sources") | MVP writes ratings, narratives and history back to Snowflake for Gainsight and Salesforce (Proposal slides 2, 4) |
| Refresh cadence | Open item, three a day vs once a day (`docs/01-product/open-items.md` row 2) | Closure adds the condition: daily, with three a day subject to cost, API limits and alert stability (Closure slide 9); Proposal says daily (slide 4) |

## Open questions

- Was the 8 Dec 2026 board-meeting view met by the MVP date, or separately? Sources only state the need (Closure slide 6).
- Which hosting and AI boundary did NAVEX sign off? The sources list it as a decision, not its outcome (Proposal slide 4).
