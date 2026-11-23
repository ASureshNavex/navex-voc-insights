# 11 Account RYGG scoring (June 2026 v3)
Sources: NAVEX RYGG Account Model.pdf and .docx ("Account Model -- Consumer Guide, June 2026 v3", all sections); skills step-1a..1d (Scoring Model, Phases 1-2, 8, Error Handling); step-2 (issue review); step-3 (sort, known data issues); NAVEX_VoC_At_Risk_2026-11-02_1.html footer.

This is NAVEX's current account rule set, the input `docs/` waits for (HLD "12. Risks and open decisions" item 2; open-items item 9).

## Already in docs/ (read there, not here)

- Terms Churn language, ARR at risk, ARR tier, Rating, Rule or trigger, Issue status: `docs/01-product/glossary.md`.
- How the platform must apply a versioned rule set (deterministic, recorded version): `docs/01-product/requirements.md` "REF-05"; storage in `docs/02-architecture/lld.md` "3.2 Data dictionary" (`account_rating`).
- Default sort, Red with churn language first: `docs/01-product/requirements.md` "ACC-14".
- Status confirmation and dead band before alerting: `docs/02-architecture/lld.md` "5.2 Status confirmation".

## Model in one paragraph (guide p.1)

Four ratings: Red / Yellow / Green / Gray. One rating per account per 30-day rolling window, recalculated fresh each run. OR logic: any single rule fires the rating; there are no weights and no numeric score. ARR sets review priority within a rating, never the rating. NPS and CSAT are context, not scoring inputs (but see AY4). Data: Enterpret Wisdom Knowledge Graph.

## Signals (per account, last 30 days unless stated)

| Signal | Definition | Query |
|---|---|---|
| complaints_30d | Distinct records with a COMPLAINT theme, non-MISC | Batch 1 |
| neg_sent_30d | Distinct records with sentiment label `Negative` | Batch 2 |
| cases_30d, cases_90d | Distinct Support Case records in 30 and 90 days (Support Cases only) | Batch 3 |
| case_ratio_30d_vs_90d | cases_30d / cases_90d; 0 when cases_90d = 0 | computed |
| churn language | `fi.content` contains a departure phrase, after post-filter | Batch 4 |
| negative CSAT | Negative-sentiment CSAT record (guide only) | none in skills |

Complaint and negative sentiment are independent measures: complaint is a taxonomy classification, negative sentiment is detected tone. Negative signal = complaint OR negative sentiment (guide Glossary).

## Rules

Evaluation order in the skills: AR4 -> AR1 -> AR2 -> AR3 -> AY1 -> AY2 -> AY3; first match wins, Red overrides all (step-1a "Scoring Model").

| Rule | Rating | Fires when | Trigger type |
|---|---|---|---|
| AR4 | Red | Any feedback record contains explicit churn / departure language (post-filtered) | Churn language |
| AR1 | Red | complaints_30d >= 5 | Volume count |
| AR2 | Red | neg_sent_30d >= 3 | Sentiment count |
| AR3 | Red | cases_30d >= 4 AND ratio >= 0.50 | Case recency spike |
| AY1 | Yellow | 3 <= complaints_30d <= 4 | Volume count |
| AY2 | Yellow | 1 <= neg_sent_30d <= 2 AND complaints_30d >= 1 | Sentiment + complaint |
| AY3 | Yellow | cases_30d >= 2 AND ratio >= 0.40 | Case recency trend |
| AY4 | Yellow | Any negative CSAT sentiment record AND complaints_30d >= 1 (guide only; absent from skills) | CSAT + complaint |
| Green | Green | >= 2 records; mix positive, neutral or praise; no Red or Yellow rule fired | Default healthy |
| Gray | Gray | < 2 records; Red always overrides Gray | Insufficient data |

Rationale given (guide): 5 complaints a month is about one a week, systemic; 3 negative interactions signal a deteriorating relationship; > half of 90-day case volume in one month is a behavioural threshold; one churn statement alone is the warning.

## Churn language (AR4) detection (step-1a Batch 4 and post-filter)

1. Match `fi.content` (last 30 days) against departure phrases, for example: not renewing, switching to another, leaving navex, canceling/cancel their / because / due to / services, backed out of, pulled out of, evaluating other vendors, evaluating alternatives, considering other vendors / leaving / not renewing, moving away from navex, replacing/replace navex, another vendor / provider / platform / solution, churn risk, at risk of losing, non-renewal, penalty clause, churning.
2. Hard-exclude false positives: cancel the call / meeting / support request / case / ticket / request, canceling an, switching to another browser / office / microsoft / a new computer, switching browser, cancel a translation, cancel professional translation, cancel services that were mistakenly, replace navex tier (an EthicsPoint tier configuration action; added 2026-09-28, present in step-1a only).
3. Require at least one explicit departure phrase to survive.
4. Manually review edge cases, for example "churn risk" written as an internal CXM note rather than customer intent. Ambiguous -> exclude and flag in churn_note.
5. churn_note = first surviving signal, truncated to 200 chars. Keep all surviving rows as AR4 verbatims, untruncated.

## Segments and ARR cohorts

Rules and thresholds are identical for every segment; segments only change the query scope and output files.

| Skill | Scope | ARR filter |
|---|---|---|
| step-1a (all segments) | No segment filter | ARR > 50,000 by default (adjustable, for example > 100K) |
| step-1b MidMarket | segment = `MidMarket` | 0 < ARR <= 50,000 |
| step-1c SMB | segment = `SMB` | 0 < ARR <= 50,000 |
| step-1d Enterprise below 50K | segment = `Enterprise` | 0 < ARR <= 50,000 |

- Segment scoping replaces volume capping: > ~150 Red + Yellow accounts in one pass -> warn, never drop (step-1b..1d).
- Regional segments (UK&I, N&W Europe, ROW, DACH, Japan) appear only via step-1a (> 50K); no below-50K skill covers them.
- Report tier attribute: `above50k` when ARR >= 50,000, else `below50k` (step-3).

## Ordering and review

| Item | Rule |
|---|---|
| Red sort | AR4 accounts first (ARR desc), then remaining Red (ARR desc) |
| Yellow sort | ARR desc |
| KPI totals | All accounts meeting a rule, regardless of ARR (guide "Key principles") |
| Week-over-week (Red only) | new_red = this - last; dropped_red = last - this; retained = both. New Red listed by rule priority AR4 -> AR3 -> AR1 -> AR2, then ARR desc; AR4 flagged CHURN. Runs only when a prior-week Red file is supplied |
| Issue review (Red only) | Each Red account labelled open / closed / norecords from Enterpret Issues (rules in 12) |

## 90-day trend column (guide; not present in current outputs)

| Element | Meaning |
|---|---|
| 2 light gray bars | Support case counts 60-90 and 30-60 days ago (account baseline) |
| 4 coloured bars | Current 30 days in weekly bands, oldest to newest |
| Dashed line | Account's 90-day average baseline |
| % negative signals | Share of all signals (all sources, 90 days) that were complaint or negative sentiment |
| Trend label | spike/increasing, sustained elevated, declining, stable |

## Edge cases (step-1a Error Handling)

| Situation | Action |
|---|---|
| ARR 0, null or missing | Exclude account |
| cases_90d = 0 | Ratio 0; AR3/AY3 cannot fire |
| Batch returns 0 rows | Warn, continue |
| No complaint verbatims | Summary from taxonomy chips |

## Conflicts with docs/

- Rule codes: `docs/01-product/requirements.md` "ACC-04" defines AR1 New red this week, AR2 Repeat red, AR4 Churn language, AY1 Green to yellow, AY2 Yellow repeat, AY3 Red to yellow, AG0 no rule. Source: AR1-AR3 and AY1-AY3 are signal thresholds (table above); week-over-week change is not a rule (guide "Quick reference"; step-1a).
- Ratings: `docs/01-product/glossary.md` "Rating" lists Red, Yellow, Green; source has four, Gray = fewer than 2 records (guide p.1). FRD FR-ACC-03 and open-items item 9 hold this as to confirm.
- Score: glossary "Friction score" (0-100 per account per week) and LLD "3.2" `account_rating.score` assume a numeric score; the source model is rule-only OR logic with no score.
- New yellow: glossary and `docs/02-architecture/lld.md` "5.3" define New Yellow as green last week; sources compare Red sets only (step-1a Phase 8) and mark "New This Week" as not in last week's run.
- Scoring output: the skills output Red and Yellow only (no Green/Gray rows); requirements "ACC-14" sorts Green accounts too.
- Fresh each run vs confirmation: guide says ratings are recalculated fresh each run; LLD "5.2" holds the confirmed status inside a dead band (affects alerts and confirmed state).

## Open questions

- AY4: in the guide (PDF and docx) but not in any skill or report footer ("Yellow rules AY1-AY3"); also contradicts "CSAT is context, not a scoring input".
- Evaluation order: guide treats Red rules as any-one; skills fix AR4 first. Only matters for which rule code is recorded.
- Churn keywords: guide lists "RFP", "cancellation", "switching", "cancel"; the skill phrase list has none of "RFP" or bare "cancel".
- ARR display threshold: guide says rows show accounts >= 100K; skills default to > 50K and reports show both tiers. Also > 50,000 (step-1a) vs >= 50,000 (render tier): an account at exactly 50,000 lands in the below-50K cohort but is tagged `above50k`.
- Green requires a "positive, neutral or praise" mix: how is that tested, and what does a non-firing negative mix rate?
- "Records" in the Gray rule (< 2): all sources, any theme?
- Negative-sentiment match: `sp.label = 'Negative'` (account skills) vs `CONTAINS 'NEGATIVE'` (domain skill).
