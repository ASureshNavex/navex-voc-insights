# 03 Scope: MVP, Phase 1 and Target State
Sources: NAVEX_VoC - Phase_1_and_Target_State_Scope.xlsx (sheets Phase 1 scope, Target State scope, Dependencies); NAVEX_VoC_Solution_Proposal.pptx slide 4; NAVEX VoC - Discovery Closure Document.pptx slides 7, 9; Navex VoC - FRD.docx 1.3; NAVEX_VoC_Features_Gap_Assessment_Usecases_Potential Solution Paths.xlsx (sheets Feature Summary, Solution Approach).

## Already in docs/ (read there, not here)

- Phase 1 and Target State capabilities with their open points, plus scope dependencies (scope workbook copied word for word): `docs/reference/phase-scope-workbook.md` "Phase 1 scope", "Target State scope", "Dependencies".
- Phase table with dates: `docs/01-product/overview.md` "Phases".
- MVP build list, items removed from the MVP, later-phase list: `docs/01-product/requirements.md` (whole file), "Removed from the MVP", "Later phases".
- FRD in-scope and out-of-scope lists: the FRD (`Navex VoC - FRD.docx`, outside this repository) "1.3.1 In-Scope", "1.3.2 Out of Scope".
- Scorecard items carried over into the MVP (fired rule, confidence, exec sponsor, AE, ARR tier, super product family, issue status, churn-language flag): `docs/02-architecture/hld.md` "2. Scope baseline after customer feedback", row "Parity items". Closure slide 9 also lists segment summary cards, region and segment filters, and the AI disclaimer.

## Milestone plan (Proposal slide 4)

| Milestone | When | Contents | Exit criterion |
|---|---|---|---|
| M1 MVP | Mobilise and validate 26 Oct - 6 Nov; build and integrate 9 - 27 Nov; test and launch 30 Nov - 8 Dec 2026 | Daily refresh of every in-scope account, reconciled with Snowflake; evidence-linked AI narratives written back to Snowflake for Gainsight and Salesforce; role-based CXM view; governed knowledge hub with admin upload and approval; Enterpret connectivity and platform foundations | Live, used by CXMs, no manual effort |
| M2 Phase 1 | Jan - Feb 2027 | Curated report library built on existing Claude skills (e.g. QBR briefs); self-serve research for Product; automated product domain friction report; AE account view (to be scoped); curated reports for the ELT and business stakeholders | In use by Product, Sales, ELT and business |
| M3 Target State | From Mar 2027 | More Fact Base sources via MCP (e.g. Pendo, Klue); a Fact Base agent automates insight delivery; on-demand briefings for Product | Product gets grounded intelligence on demand |

Milestone 1 decisions listed as open (Proposal slide 4): AI boundary (Cortex or Claude direct); source of truth for ratings; knowledge hub storage; where CXMs work; acceptance criteria and sign-off; Snowflake access in week 1.

## Phase view from discovery closure (Closure slide 7)

| Phase | Audience | Status (as of Nov 2026) | Capabilities | To confirm |
|---|---|---|---|---|
| MVP | Customer Success | For sign-off | At-risk scorecard in one view, with themes and verbatims beside each rating; daily refresh; change-of-status alerts; access from SSO and the org chart; Gainsight link to the account; usage and audit | Refresh three a day vs daily; Gainsight CTA set up by NAVEX; churn score availability; access levels for ELT and Sales; knowledge hub uploads by VoC admin only (Closure slide 9) |
| Phase 1 | Product | In definition | Monthly Product Friction Report; account-level product briefs for customer meetings; thematic product briefs as planning evidence; deep dives next | Self-service report generation; actions raised in Gainsight or Salesforce; routing of renewals inside the 180-day window |
| Target State | Enterprise | In definition | Monthly Fact Base across competitive, market, customer and internal insight; Aha! integration linking the monthly report to the product fact base and analysis to an opportunity or initiative | Further sources and audiences; QBR generation |

Phase 1 and Target State acceptance criteria and success measures are left to their own refinement sessions (Closure slide 7).

MVP acceptance at sign-off (Closure slide 9): parity with the current scorecard; stable daily refresh; change-of-status email alerts; SSO and role-based access; Gainsight link to the account. Prototype additions beyond today's scorecard, including CXM commentary, are held for later prioritisation (Closure slide 9).

## Function count by milestone (Gap xlsx, sheet Feature Summary)

| Module | Functions | MVP | Phase 1 | Target State | To confirm |
|---|---|---|---|---|---|
| 1 Account Intelligence | 22 | 19 | 0 | 0 | 3 |
| 2 Product Intelligence | 10 | 0 | 8 | 2 | 0 |
| 3 Reporting | 4 | 0 | 4 | 0 | 0 |
| 4 Data and Integration | 18 | 13 | 1 | 1 | 3 |
| 5 Platform Foundations | 17 | 17 | 0 | 0 | 0 |
| Total | 71 | 49 | 13 | 3 | 6 |

F-39, marked "MVP / Phase 1", is counted under "To confirm" in module 4. Function detail: `04-feature-gap-assessment.md`.

## Phase placement disagreements among the sources

| Capability | Placements found |
|---|---|
| AE / Sales leadership views | Phase 1, to be scoped (Proposal slide 4; Gap xlsx F-36); Target State, phase to confirm (Scope xlsx, Target State sheet) |
| ELT, executive and Finance reports | Phase 1 (Proposal slide 4; Gap xlsx F-35); Target State (Scope xlsx, Target State sheet) |
| QBR report | Phase 1 or later (FRD 1.3.2); Phase 1, via QBR briefs (Proposal slide 4); open in Target State (Closure slide 7); a separate release only if the account brief does not cover it (Scope xlsx, Dependencies) |
| Account brief | Phase 1 (FRD 1.3.2); MVP (Closure slide 9) |
| Call transcripts | Not used for MVP scoring (FRD 1.3.2, FR-BKE-02); placement to confirm after evaluation (Scope xlsx, Target State sheet; Gap xlsx F-43) |
| Churn score beside the rating | Combining the two is out of scope (FRD 1.3.2); availability for the MVP to confirm (Closure slide 9); "To confirm" (Gap xlsx F-18); a separate scope decision (Scope xlsx, Dependencies) |
| Knowledge context in account narratives | MVP (Gap xlsx F-09); knowledge hub evidence for Product research proposed for Phase 1 (Scope xlsx, Phase 1 sheet) |
| Snowflake write-back of ratings and narratives | MVP (Proposal slide 4; Gap xlsx F-50 to F-52, explicit in the RFP) |
| CXM commentary handoff to Gainsight | Placement to confirm, "Phase 1" in comments (Scope xlsx, Phase 1 sheet); Phase 1 (FRD 1.3.2) |
| Knowledge hub contributions beyond admins | Late Phase 1, to confirm (Scope xlsx, Phase 1 sheet); TBC for the MVP (FRD FR-KHV-02, FR-LKN-01); admin only in the MVP (Closure slide 9) |

## Conflicts with docs/

| Topic | docs/ | Source |
|---|---|---|
| Phase dates and names | Phase 1 9 Dec 2026 - 15 Feb 2027; "Phase 2" 16 Feb - 30 Mar 2027 (`overview.md` "Phases") | Phase 1 Jan - Feb 2027; "Target State" from Mar 2027, no end date (Proposal slide 4) |
| Phase 1 contents | Product workspace, research agents, knowledge hub files as evidence, Gainsight write-back (`overview.md` "Phases") | Also the curated report library, AE view and ELT/business reports (Proposal slide 4). Gainsight handoff placement still to confirm (Scope xlsx, Phase 1 sheet) |
| Enterprise views | "Phase 2" (`overview.md` "Phases") | Phase 1 (Proposal slide 4) or Target State (Scope xlsx) |
| Snowflake write-back | Not in the MVP; Snowflake read only; downstream writes "in a later phase" (`overview.md` "Data sources", "Rules that shape every decision") | MVP: narratives written back to Snowflake for Gainsight and Salesforce (Proposal slide 4; Gap xlsx F-50 to F-52) |
| Knowledge hub upload in the MVP | CXM leadership uploads, VoC admins approve (`hld.md` section 2, row "Knowledge hub") | VoC admin uploads only, not in the CXM view (Closure slide 9) |
| Churn score in the MVP | In the MVP, side by side with the rating, definitions to confirm (`requirements.md` ACC-09) | Availability to confirm at sign-off (Closure slide 9); a separate scope decision (Scope xlsx, Dependencies) |

## Open questions

- Which phase plan is current, the Proposal's (Oct 2026) or the dates in `docs/01-product/overview.md`? The sources in this slice do not settle it.
- Did the Snowflake write-back stay in the MVP after the Closure (Nov 2026)? Closure slide 9 does not mention write-back.
