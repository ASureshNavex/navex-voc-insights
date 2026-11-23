# 10a Product domain RYGG scoring (hybrid percentile model)
Sources: NAVEX Domain Model July 2026.pdf ("VoC Product Domain Scoring -- How It Works", p.1-3 and "At a glance" page); weekly-voc-html-report skill (Steps 2, 2A-2D, Maintenance, Error handling); NAVEX-VoC-Domains-September 2026.html (footer, structure only).

Scores each of the 14 product domains (list in `10-domain-model.md`) against its own history. Separate from the account model in `11-rygg-account-scoring.md`.

## Already in docs/ (read there, not here)

- Product Domain Friction Report and deep dives are later-phase scope: `docs/01-product/requirements.md` "Later phases"; detail in `docs/reference/phase-scope-workbook.md` (Product Domain Friction Report, Report-linked deep dives).
- Nothing in docs/ states the domain scoring rules; they are in full below.

## Purpose and cadence (Domain Model p.1, p.3)

| Item | Value |
|---|---|
| Ratings | Red (action), Yellow (watch), Green (normal), Gray (insufficient history) |
| Scoring window | Last 30 days, anchored to run date |
| Baseline window | Nov 1, 2025 to run date, rolling; grows each run; thresholds recalculated fresh each run |
| Cadence | Monthly, ahead of Product Business Review (PBR) materials |
| Audience | Product, engineering and design leadership; a separate weekly account-level report goes to customer-facing teams |
| Format | Self-contained HTML, expandable domain rows; per-domain deep dive files on request |
| Confidence label | 90% (+/-5%), "fixed per team alignment" (Domains output footer) |

## Inputs per domain (weekly skill Step 1)

| Query | Measure | Window |
|---|---|---|
| 2A | Complaint count, `COUNT(DISTINCT nli.record_id)`, complaint theme, non-MISC | 30 days; high tier also last complete week |
| 2B | Negative-sentiment count (`sp.label CONTAINS 'NEGATIVE'`) | 30 days |
| 2C | Distinct accounts with complaints (breadth) | 30 days |
| 2D | Top 7 complaint themes by record count | 30 days |
| 2E / 2F | Complaint records and accounts by region / by segment | 30 days |
| 2G | Weekly complaint counts, 8 most recent complete weeks | Sparkline only |
| Baseline | Weekly complaint series from 2025-11-01 to run date (`toStartOfWeek`) | Full baseline |

## Baseline statistics (Step 2A)

From the weekly series per domain: `median_weekly`; `p75_weekly`, `p90_weekly` (linear interpolation); `rolling_sums` = every rolling 4-week sum; `p75_rolling`, `p90_rolling`; `baseline_weeks`; `volume_tier`.

## Volume tiers

| Tier | Median weekly complaints | Scored on | Static members (skill) |
|---|---|---|---|
| High | >= 50 | Most recent complete week vs weekly P75 / P90 | EthicsPoint IM, Performance/Reliability, Usability, NAVEX One |
| Mid | 10-49 | Rolling 30-day sum vs P75 / P90 of historical rolling sums | PolicyTech, CT Tech |
| Low | < 10 | Same as Mid | Disclosure, RiskRate, GRC Insights, CT Content, IRM/LockPath, Regulatory Change, WhistleB, Nira |

Reason (Domain Model p.1): a monthly window dilutes single-week spikes for high-frequency domains; a shared threshold would misclassify domains of different volume.

## Rating rules (Step 2B; first match wins)

High tier:

    last_week = complaints in most recent complete 7-day week before run date
    if last_week >= 100            -> Red    (AF, absolute floor, checked first)
    elif last_week >= p90_weekly   -> Red    (R1-weekly)
    elif last_week >= p75_weekly   -> Yellow (Y1-weekly)
    else                           -> Green

Mid and Low tier:

    rolling_30d = complaints in the 30-day window
    abs_floor   = round(median_weekly * 4.3)
    if rolling_30d >= p90_rolling and rolling_30d >= abs_floor -> Red    (R1-rolling)
    elif rolling_30d >= p75_rolling                             -> Yellow (Y1-rolling)
    elif rolling_30d > 0 and rolling_30d >= abs_floor           -> Yellow (Y1-floor)
    else                                                        -> Green

All tiers:

| Rule | Condition | Result |
|---|---|---|
| R4 breadth | distinct_accounts >= 1.25% of the domain's subscriber base AND >= 10 | Red regardless of tier; cannot fire if subscriber base unknown (show a dash) |
| Gray | baseline_weeks < 16 | Gray regardless of volume |
| Y1-floor guard | median_weekly = 0 (abs_floor = 0) | Y1-floor disabled; must reach p75_rolling. Skill names WhistleB and Regulatory Change; a Yellow via Y1-floor on them is a bug, force Green |

- AF is a single auditable threshold (100/week), same for all four high-tier domains; do not tune per domain (Decided, weekly skill).
- Every rating stores: rating, triggered rule, tier, threshold values.

## Trend flag (Step 2C; never changes the rating)

| Source | Fires when |
|---|---|
| Domain Model p.2 | Recent 4-week average >= 50% above prior 8-week average |
| Weekly skill | recent_4wk_avg >= 1.5 x prior_8wk_avg AND recent_4wk_avg >= 15/week AND >= 12 weeks of baseline |

Display: "Trend: 4-wk avg (X/wk) is Y% above prior 8-wk avg (Z/wk)"; omit entirely when not fired.

## Display thresholds (Step 2D)

| Value | Formula | Shown as |
|---|---|---|
| median_monthly | round(median_weekly x 4.3) | "typical month" |
| watch | p75_rolling (mid/low) or round(p75_weekly x 4.3) (high) | "watch" tick |
| action | p90_rolling (mid/low) or round(p90_weekly x 4.3) (high) | "action" tick |
| abs_floor, baseline_weeks, per-domain median_weekly | as above | footer |

Sort: within each band (Red, Yellow, Green, Gray), by 30-day complaint volume descending; never by taxonomy number.

## Expected actions (Domain Model p.2)

| Rating | Meaning | Action |
|---|---|---|
| Red | Volume in the top 10% of weeks for this domain | Investigate driving themes; review related roadmap work; choose product fix, support intervention or outreach |
| Yellow | Above watch (top 25%), below action | Monitor; consider proactive customer communication or support alert; make the product team aware |
| Green | Within normal range (can be Green with triple-digit counts) | No immediate action; note persistent low-volume themes |
| Gray | Fewer than 16 weeks of baseline | Check Enterpret channel coverage; Gray does not mean "no problems" |

## Model history (Domain Model p.2)

| Generation | Rule | Outcome |
|---|---|---|
| 1 | Fixed: Red at 30 complaints, Yellow 10-29 | No empirical basis; same standard for all sizes |
| 2 | Red at 1.5 x rolling 12-week median | Short baseline depressed medians; most domains Red at once |
| 3 (current, Decided) | P75 watch / P90 action of own weekly history; high tier weekly, others rolling 30-day | Back-test caught every real spike without over-firing |

## Maintenance

| When | Activity (Domain Model p.3; weekly skill) |
|---|---|
| Every run | Self-calibrates; check Gray domains that graduated. Skill: recompute median_weekly and re-classify tiers, log in footer |
| Quarterly | Fire-rate audit: last 3 months; a domain Red every run means a loose threshold. Skill target for high-volume domains ~10% Red, ~15% Yellow, ~75% Green; review whether the 100/wk floor alone keeps a domain Red |
| Quarterly | Tier check: move a domain whose typical weekly volume shifted > 30% |
| On structural event | Release, migration or support model change: assess or reset the pre-event baseline |
| Annually | Parameter review of P75/P90 (and floor); only on 3+ months of systematic miscalls |

## Error handling (weekly skill)

| Situation | Behaviour |
|---|---|
| 0 records in window | Gray if baseline_weeks < 16, else score normally |
| Query timeout | Skip row; footnote "data unavailable" |
| PRAISE-only themes | Zero negative signals; Gray |
| Breadth unavailable | Dash in Accounts column plus footnote |
| All domains Green/Gray | Omit Red/Yellow dividers; note "No high or moderate risk domains this period" |

## Conflicts with docs/

- None found: docs/ does not define domain scoring. `docs/01-product/glossary.md` "Rating" (Red, Yellow or Green) is account-level; domain ratings include Gray.

## Open questions

- Tier review: Domain Model p.2 says tiers are reviewed quarterly (> 30% shift); the weekly skill re-classifies every run. The Sept 2026 output's listed medians would place some domains (for example PolicyTech, CT Tech) in a different tier from the static table.
- Zero-median guard: the skill names WhistleB and Regulatory Change as median 0, but the Sept 2026 output footer lists non-zero medians for both. Which rule applies when the median is small but not zero?
- Mid/Low window: thresholds come from rolling 4-week (28-day) sums but the scored value is a 30-day sum.
- Source filter: Domain Model p.1 says Issues and Product Ideas are context only, but Query 2A counts complaint records from every source (no `nli.source` filter).
- Trend flag thresholds differ between the PDF and the skill (see table).
- R4 needs a per-domain subscriber base; no source for it is named.
- AF, R4 and Y1-floor are in the skill and output footer but not in the July 2026 PDF; which document is authoritative.
