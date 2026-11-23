# 13 Report outputs: At-Risk, Domains, domain detail (structure only)
Sources: NAVEX_VoC_At_Risk_2026-10-05_2.html and NAVEX_VoC_At_Risk_2026-11-02_1.html (structure, labels, footers); step-3-navex-rygg-all-segments-render skill (Steps 6-9); NAVEX-VoC-Domains-September 2026.html; weekly-voc-html-report skill (Section 1-4, specs); NAVEX-VoC-EthicsPoint-Detail-2026-08-31.html; domain-detail-reports skill (Sections 1-6). No account data reproduced.

All three are single self-contained HTML files: inline CSS, no external URLs, brand accent `#FF4500`, confidence bar "90% (+/-5%)" plus AI notice ("customers may not use NAVEX terminology"). Fact Base and briefs: `13a-fact-base-outputs.md`.

## Already in docs/ (read there, not here)

- Target screen for accounts (cards, columns, filters, detail, sort): `docs/01-product/requirements.md` "SCR" and "ACC"; latest prototype `docs/reference/prototype/voc-insights-workspace-latest.html`.
- AI notice and confidence figure as configuration: `docs/01-product/requirements.md` "SCR-03".

## At-Risk Account Scorecard (step-3 output, 2026-11-02 version)

Title: "NAVEX VoC -- At-Risk Account Scorecard (All Segments)". Sub-line: run date, last 30 days, segments, both ARR tiers, Red & Yellow count.

Page order: header (4px orange top border) -> KPI tabs -> disclaimer bar -> filter bar -> table (25 rows/page) -> pager -> footnote.

KPI tabs: All / Enterprise / MidMarket / SMB, three tiles each: Total ARR at Risk (ARR + accounts), Red Accounts (count + ARR), Yellow Accounts (count + ARR). No "active accounts" tile (only available for > 50K).

Filters, in order:

| Filter | Id | Options |
|---|---|---|
| Rating | `f-rating` | Red & Yellow / Red only / Yellow only |
| Segment | `f-segment` | All + Enterprise, MidMarket, SMB, DACH, Japan, N&W Europe, ROW, UK&I |
| ARR Tier | `f-tier` | All / $50K+ ARR / Below $50K |
| Region | `f-region` | All / AMER / EMEA/APJ |
| New This Week | `f-new` | All / New This Week (n) |
| CSM / CXM, Account Executive, Exec Sponsor | `f-csm`, `f-owner`, `f-exec` | All + Blank + names |
| Super Product Family | `f-spf` | All + SPF values (see 10) |
| CXM Manager | disabled | "Coming soon" (data ingestion pending) |
| Issue Status | `f-issue` | All Accounts / Red - No Open Issue (closed or norecords) / Churn Language - No Issue (same AND AR4) / Red - Open Issue |
| Account Name | `f-search` | Text; plus Clear Filters |

Table, 10 columns:

| # | Header | Content |
|---|---|---|
| 1 | Account | Name, blue NEW chip if new this week, SPF list |
| 2 | ARR | Right-aligned, `$XK` / `$X.XM` |
| 3 | Region / Segment | Region text + segment chip |
| 4 | CXM / Exec Sponsor | CXM + "Exec: <name>" chip |
| 5 | Account Executive | From Snowflake owner |
| 6 | Next Renewal | `Mon DD, YYYY` or "Data ingesting" |
| 7 | Rule / Trigger | Rule chip (AR red, AY yellow) + stats, e.g. "<n> complaints, <n> neg sentiment, <n> cases 30d / <n> 90d (ratio 0.xx)", or the churn note |
| 8 | NPS | Promoter / Passive / Detractor badge + date, or "No data" |
| 9 | Issue Status | Red: open chip "<n> open" + "<total> total, last <date>" (+ Health Data Action note); gray "All issues closed"; bold red "Churn language -- no issue" (AR4) or "No issue records". Yellow: "Not checked". No issue data: "Coming soon" |
| 10 | Taxonomy & Summary | Up to 4 L1 chips, L3 list, summary; AR4 rows add a "Churn detail" disclosure with "CXM Notes" and the first AR4 verbatim |

- Divider rows (not paginated): Red "HIGH RISK -- RED -- AR4 churn language first, then ARR" with counts (Red, with churn language, of those without open issue, Red without open issue, with no records, ARR); Yellow "ELEVATED RISK -- YELLOW -- sorted by ARR" with count and ARR.
- Row `data-*`: name, rating, region, segment, owner, exec, csm, spf (pipe-delimited), tier (`above50k`/`below50k`), issue (`open|closed|norecords|unchecked`), ar4, new.
- Rows striped `#FFFFFF` / `#F7F9FC`, re-indexed per page.
- Footnote: data sources, exec map, NPS rule, scoring model and rules, issue status rules and current split, segment tab behaviour (regional segments only in All), known gaps.

Earlier 2026-10-05 version (single cohort, > 50K): title "VoC Report -- Account RYGG Scorecard (Last 30 Days)"; 5 KPI tiles (Total ARR at Risk, Red, Yellow, New This Week split Red/Yellow, Accounts Active in Enterpret); no Rating, Tier or Issue filters; column 9 "Open Issues" = "Coming soon".

## Domains report: Product Domain RYGG Scorecard

Title "NAVEX VoC Report -- Product Domain RYGG Scorecard"; meta: Last 30 Days, run date, window dates, segment/region if filtered. Sections: header + confidence bar -> scorecard (heading with 4px orange bar, sub "Full historical baseline (Nov 1, 2025 - run date), Last 30 Days, Hybrid percentile model", legend bar) -> cross-cutting callout (if triggered) -> footer.

| Column | Content |
|---|---|
| Product Domain | Bold name, optional sub-label |
| Rating | Badge with dot: Red / Yellow / Green / Gray |
| 30-Day Complaint Volume | CSS bar to action level, amber "watch" tick, red "action" tick (when >= 0.8 of action), sub-line "typical month ~X, watch at Y, action at Z", count, status badge: below typical / near typical / above typical / at action level / no baseline |
| Neg. Sentiment | Count or dash |
| Accounts | Distinct accounts or dash |
| Signal by Region & Segment | Region chips AMER, EMEA, APAC; segment chips Enterprise, Mid-Market, SMB, Strategic; "LABEL PCT% count"; zero chips at 0.5 opacity |
| Primary Trigger | Plain-language headline (e.g. "<n> complaints this month -- above watch level"), sub-line with medians and thresholds (rule codes only here), optional amber trend line |
| What's Driving Complaints | 4-6 theme chips above one summary sentence, no scoring language |
| Related Roadmap Work | Up to 4 Aha! items "ID, name, status badge" (In progress, Ready to ship, Shipped, Planned); blank if none |

- Each domain = 3 rows: data row, toggle row ("Show complaint detail" / "Hide complaint detail", 3px domain separator), drawer row (hidden). Drawer grid 1fr / 1.4fr / 0.8fr: top 7 theme bars; 3-paragraph narrative with bold leads (Gray: one paragraph); 8-week sparkline (gray normal, red spike, orange current) + 3 shift bullets (new, growing, shrinking, steady).
- Divider rows: Red -- High Risk, Yellow -- Moderate Risk, Green -- Normal Range, Gray -- Insufficient History.
- One JS function `toggleDrawer`. Region chip colours are the only use of the secondary palette.
- Footer: source, window, run date, full threshold summary, per-domain weekly medians, PRAISE-only excluded, General resolved, sort rule.

## Domain detail report (per domain)

File `NAVEX-VoC-<Slug>-Detail-<date>.html`; title "<Domain> -- Source Feedback Detail"; meta: window, run date, records, accounts.

| Section | Content |
|---|---|
| KPI bar (6 cards) | Total (unique) records, distinct accounts, support cases, issues (escalations), product ideas, Red / Escalation |
| Theme chart | Top 8 complaint themes, clickable; filters the table; "Filtered to N records" note + Clear filter |
| Legend | Source badges (Support Case, Issue, Product Idea), severity (Red-flagged issue, Escalation), Salesforce and Enterpret link icons |
| Table | Date / Source, Account, Theme & Summary (chips + one-line case subject, chevron), Record Link (Salesforce always visible, Enterpret); newest first; no row limit |
| Drawer per row | Left: case subject + full AI summary. Right "Context": source and issue type, theme also in other domains, "Active churn / escalation signal", other records for the same account |
| Footer | Source, explicit window, L1 filter, dedup on record_id, PRAISE-only and MISC excluded, link notes, record and account totals |

JS limited to `toggleRow` and `filterTheme` / `applyFilter` / `clearFilter`. Zero records: header + zero KPIs + "No complaint records found ...".

## Conflicts with docs/

- Column order: `docs/01-product/requirements.md` "ACC-01" puts Issue status before NPS; the At-Risk report has NPS (8) before Issue Status (9).
- Rating filter: "ACC-06" has Red, Yellow, Green multi-select plus Theme, Renewal window and Sort; the report has Red & Yellow / Red only / Yellow only and no Theme, Renewal or Sort filter, plus a disabled CXM Manager filter.
- Churn detail: "ACC-05" shows the fired rule and up to three verbatims with source and date; the report shows one AR4 verbatim labelled "CXM Notes".
- Segment cards: "SCR-06" selecting a card sets the segment filter; step-3 Step 4 says KPI tabs are display-only, while the 2026-11-02 output footer says a tab filters the table.
- Rating cards: "SCR-04"/"SCR-05" have New red / Repeat red / New yellow lists; the report has only a NEW chip and a New This Week filter.

## Open questions

- Region model: weekly skill expects AMER / EMEA / APAC chips; the Sept 2026 output shows EMEA/APJ combined ("APAC breakdown unavailable").
- Segment chips: skill lists Enterprise, Mid-Market, SMB, Strategic; Snowflake values are MidMarket and regional segments, and no "Strategic" value is seen.
- Detail window: the skill uses run date minus 30 days; the EthicsPoint example covers a calendar month (2026-08-01 to 2026-08-31).
