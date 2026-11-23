# 13a Fact Base and research brief outputs (structure only)
Sources: Navex_Voc_FactBase_HTML_Skills.zip: navex-qbr-factbase.skill (SKILL.md), NAVEX_September2026_FactBase (1).html, retaliation-tracking-brief (2).html, one account product brief HTML (customer-named file; structure only). No customer data reproduced.

## Already in docs/ (read there, not here)

- Fact Base is later-phase scope: `docs/01-product/requirements.md` "Later phases"; product needs in `docs/reference/phase-scope-workbook.md` rows "Four-quadrant Fact Base report", "Living Product Fact Base", "Initiative Fact Base", "Competitive and market intelligence", "Aha! evidence and commentary handoff".

## QBR Fact Base (navex-qbr-factbase skill)

One single-slide PPTX per product domain per period, for product leadership. Built by editing the fixed template `FactBase_Template.pptx` (slide XML text replacement; never rebuilt from scratch, to keep branding).

| Slide area | Content | Source |
|---|---|---|
| Top band, full width | Competitive & Market Intelligence: 3 competitor cards, 3-4 bullets each | Klue "What's New" cards, Blindspot interviews (label exactly "Blindspot Interviews") |
| Bottom left | Customer Insights: top voted Aha! ideas (vote badge + description), 1-2 NPS/CSAT verbatim boxes, UG/NCC synthesis note, new idea submission themes (3 chips + descriptions) | Aha!, Enterpret, uploaded UG/NCC notes |
| Bottom right | Internal Signals: top support case themes (up to 7 count badges + descriptions, label "Enterpret, N complaints"), Pattern callout, Go-To-Green callout | Enterpret, Go-To-Green export |
| Footer | Sources line | |

Workflow (Decided in skill):

| Phase | What | Gate |
|---|---|---|
| 0 | Confirm period with exact date bounds, domains, current-period uploads (UG, NCC, Go-To-Green) | Ask if missing |
| 1 Collect | Per domain, data only: full Klue landscape scan, Aha! top / new / vote activity, Enterpret complaint total and top themes, Go-To-Green and UG/NCC tags | Multi-domain only |
| 2 Findings brief | In chat, per domain: complaint signal (or "low volume" under ~60), competitor movement, Aha! signal, corroboration, flag Build / Skip / Build -- high signal / Skip -- nothing new | Hard stop for user sign-off |
| 3 Build | Approved domains: quotes via `find_user_quote` only, draft, build, validate, render to image, visual QA, present | Every slide QA'd |

Rules:

- Enterpret: exact L1 names (confirm with a graph value search), explicit `toDateTime` period bounds; full build pulls COMPLAINT / IMPROVEMENT / HELP theme breakdown, total complaints with citation URL, NPS/CSAT quotes.
- Never quote from memory or paraphrase into quote marks. Low-volume domains (often 10-60 complaints) may carry one synthesized "verbatim-style" box, labelled synthesized.
- Aha!: scope by the `Owning Product` custom field (resolve its numeric id each run), cross-check `R/C Product`; capture votes, workflow status, linked initiative id; check `duplicate_of` and `admin_response` before calling an idea an open gap.
- Go-To-Green is secondary validation only, never a primary source of new claims; build an account-to-domain map once per run.
- Cross-check that the three areas tell one story; make corroboration explicit.
- Domain catalog: 10 Fact Base domains with Aha! Owning Product and Enterpret L1 name (table in `10-domain-model.md`); competitor names are search anchors, not the set to report.

## Fact Base HTML (September 2026 example)

Page: title "NAVEX -- <Month YYYY> Fact Base", sub "All Domains (High Signal + Standard Signal), <date range>". One card per domain:

| Card part | Content |
|---|---|
| Header | Domain title, signal pill (High Signal / Standard Signal), period |
| Competitive band | "Competitive & Market Intelligence", competitor columns (name + body) |
| Customer Insights column | Top Ideas (Aha!) with vote badges; NPS / CSAT Verbatims (Enterpret, period) quote boxes with attribution, synthesized boxes marked; Go-To-Green / UG / NCC; New Idea Themes tags |
| Internal Signals column | Top Support Case Themes (Enterpret, N complaints) rows with counts; "Pattern:" and "Go-To-Green:" callouts |

## Topic brief (retaliation tracking example)

Header label "<Product domain> -- Product Signal Brief". Sections: Signal at a Glance (KPI tiles: records touching the topic, product ARR and total ARR across impacted accounts, Aha! votes, competitor count, ideas by status) -> Business Case Anchors -> What Customers Are Asking For (distinct needs) -> Customer Voice (quotes) -> Top 10 Accounts by Total ARR with the signal (Account, Total ARR, product ARR, Segment, Region, Records) -> Aha! Ideas Inventory (status chips Future Consideration / In Development / Launched) -> Competitive Landscape (cards with threat chips Highest Threat / Watch / Lower Threat; capability matrix NAVEX now, NAVEX roadmap, competitors) -> Recommended Actions for Business Case.

## Account product brief (example)

Sections: Account Snapshot (tiles: RYGG 30-Day, RYGG 90-Day, Open Support Cases, NPS per product; snapshot fields: products, customer since, organization, total ARR) -> Product Feature & Functionality Challenges (per-product cards grouped by L2 headers, theme rows with counts, pattern callouts, active escalation fields Type / Status / Age / Links) -> Product Insights (labelled items such as Active Escalation, Recurring Functionality Bug, Recurring Friction, Platform Adoption Risk, Unmet Feature Gap) -> Aha! Roadmap Cross-Reference (Customer Theme, Category, Vol., Matched Aha! Ideas, Matched Initiatives, Status).

## Conflicts with docs/

- Layout: `docs/reference/phase-scope-workbook.md` calls it a "Four-quadrant Fact Base report"; the skill and template have three areas (one full-width band plus two bottom columns).
- Format: docs describe an in-platform report; the source skill produces PPTX slides and the example output is HTML.

## Open questions

- No skill in this source set produces the Fact Base HTML, the topic brief or the account product brief; how they are generated is not stated.
- "RYGG 90-Day" in the account brief is not defined by the account model (30-day window only).
- The 10th Fact Base domain (Content: Training / CoC / Awareness) has no Owning Product or L1 yet.
- Klue access is via its connector only; Blindspot interview availability per period varies.
