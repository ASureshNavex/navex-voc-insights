# Open questions, risks and assumptions

Sources: Navex_Notes_15_OCT_2026.txt (Notes 15 Oct, Lnnn), Navex_VoC_Meeting_Transcript.txt (Transcript, mm:ss), engagement zip text files: Response to technical questions 13 Nov (Tech answers Qn), Enterpret integration notes 13 Nov (Enterpret notes), SSO and access 3 Nov (SSO notes), Tech stack detail 13 Nov (Stack notes), Practices 3 Nov, Platform swap 3 Nov; Artifacts/NAVEX_VoC_Mockup_React_Handover.md (Handover md); Latest prototype 19 Nov (Latest).

## Already tracked in docs/

`docs/01-product/open-items.md` holds 18 open items with the assumption coded for each (knowledge hub approval, refresh frequency, response tracking, ELT and Sales modules, custom reports, account brief audience, personal digests, tooltip definitions, rating rule set and Gray, Snowflake field mapping, status confirmation tuning, Corp AD identifiers, AWS region, navigation, email service, masking and retention, session timeout and performance, Enterpret ceiling and seat). They are not repeated here. `docs/01-product/requirements.md` marks further items "Confirm" in its Status column.

## Open questions not in docs/

| # | Question | Source | Owner (role) |
|---|---|---|---|
| Q1 | Gainsight target for VoC output: Timeline activity or Plan of Action | Notes 15 Oct L436 | NAVEX Gainsight owner |
| Q2 | Does the Gainsight instance allow a home-page link or widget to the workspace | Feedback 13 Nov; Tech answers Q4 | NAVEX Gainsight administrator |
| Q3 | Org chart source (Entra manager attribute or HR feed) and its refresh cadence; TEAM scope depends on it | Tech answers Q3 | NAVEX IT |
| Q4 | Is the account ownership master authoritative and complete | SSO notes, What still needs a decision | NAVEX data team |
| Q5 | Acceptable revocation delay, which sets the scope cache window (5 minutes proposed) | SSO notes | NAVEX IT and security |
| Q6 | Who may see verbatim customer text; today a role flag with no policy owner | SSO notes | NAVEX (policy owner not named) |
| Q7 | Enterpret: maximum result size and pagination of `run_graph_query`; whether MCP and REST share a quota; citation links for all sources or some; maximum token lifetime | Enterpret notes, Open questions; Tech answers Q1 | Enterpret, via NAVEX |
| Q8 | Taxonomy depth: five-tier adaptive taxonomy or three levels | Notes 15 Oct L177 vs Enterpret notes, Fetch pattern | Psiog, confirm from `get_graph_schema` |
| Q9 | Write-back field mapping: CTA type, playbook, owner, due date, evidence in the body; Gainsight API key and Salesforce connected app (Phase 1) | Tech answers Q5 | NAVEX Gainsight administrator |
| Q10 | Dynatrace SaaS or Managed; OneAgent operator or plain OTLP exporter on Fargate | Stack notes, Observability | NAVEX platform team |
| Q11 | Domain vs product: domains have different scoring scales (one product scored differently from others); how ratings roll up across tied domains | Notes 15 Oct L456-457, L543-545 | NAVEX Product |
| Q12 | When call transcripts become a scoring source; notes expected November, MVP excludes them | Notes 15 Oct L547-550; Latest source health ("Planned for November") | NAVEX VoC model owner |
| Q13 | Who owns the copy and grammar review before build | Handover md s6 | NAVEX VoC SMEs |
| Q14 | Business cases for other departments (Finance, executive) | Notes 15 Oct L316-320 | NAVEX CSO office |
| Q15 | A neutral, centralised VoC leader was recommended; no owner named | Notes 15 Oct L322 | NAVEX leadership |

## Risks

| # | Risk | Effect | Mitigation in sources | Source |
|---|---|---|---|---|
| R1 | CXMs will not visit a separate URL | Low adoption, the stated success factor | Deep link from alert and CTA; Gainsight entry point | Feedback 13 Nov; Transcript 1:20-1:38 |
| R2 | Product team discounts Enterpret data as mostly support cases (about 80%) | No roadmap impact | Phase 1 product friction report with evidence | Notes 15 Oct L516-519 |
| R3 | Empty scope looks like "no accounts at risk" | Silent loss of alerts | App roles over group claims; overflow fallback; distinguish empty from failed resolution | Tech answers Q3; SSO notes |
| R4 | Incomplete ownership master or stale org chart | Wrong or empty books | Agree source and cadence (Q3, Q4) | SSO notes; Tech answers Q3 |
| R5 | Alerts flap on threshold accounts | Users ignore alerts | Confirmation runs, dead band, once-daily evaluation, cool-down | Tech answers Q2; Practices 7 |
| R6 | Duplicate CTAs on write-back retry | Loss of trust | Outbox with idempotency key; dead-letter queue | Tech answers Q5 |
| R7 | Action state tracked in two places diverges | Neither is trusted | Gainsight and Salesforce remain system of record; platform shows status read only | Tech answers Q5 |
| R8 | Enterpret rate limits are unpublished | Refresh throttled | Bulk delta pulls; burst probe; ask Enterpret | Enterpret notes; Tech answers Q1 |
| R9 | Enterpret token is an organisation-wide credential | Exposure of all feedback | Secrets Manager, finite expiry, rotation owner | Enterpret notes |
| R10 | Enterpret connector draws a security review | Schedule slip | Read third-party assessments before the review | Enterpret notes, Security review |
| R11 | Iframe embedding in Gainsight | Sign-in breaks under third-party cookie rules; CSP work | Deep links only for MVP | Tech answers Q4 |
| R12 | Revoked access survives the scope cache window | Up to 5 minutes of stale access | Set window to zero where needed | SSO notes |
| R13 | Feedback not matched to an account is invisible | Under-counted risk | Count unresolved records; fail the run above a threshold | Practices 2 |
| R14 | Volume ranks the loudest, fixed thresholds ignore account size | Noisy ratings | Weight by commercial context; thresholds as versioned config | Practices 4 |
| R15 | Watchlist turnover each run | Audience stops trusting it | Stability metric with a ceiling | Practices 7 |
| R16 | Data platform swap changes results | Unvalidated ratings | Re-run evaluation and re-baseline before promoting an adapter | Platform swap |
| R17 | Parallel churn prediction work elsewhere at NAVEX | Duplicated effort, two churn numbers | Keep churn score separate, labelled as a distinct measure | Notes 15 Oct L1-5, L393 |
| R18 | Schedule pressure: the MVP must land before Phase 1 starts on 9 Dec (`docs/01-product/overview.md`, Phases) | Scope squeeze | Parity-first scope; no net-new features | Transcript 40:30; Feedback 13 Nov |
| R19 | Latest prototype still contains unreachable MVP v1 screens and superseded text (approval stages, High ARR, CXM comment) | Builders copy retired copy | Build from NAV-reachable screens only (see 31-workspace-ux.md) | Latest |

## Assumptions stated in the sources

| # | Assumption | Source |
|---|---|---|
| A1 | About 1,200 accounts in scope | Tech answers Q1 |
| A2 | Three runs a day cost about 10 to 25 USD a month more than one, at list prices | Tech answers Q1 |
| A3 | Narratives regenerate only when their inputs change, so model cost is flat across refresh frequency | Tech answers Q1 |
| A4 | Bulk delta pulls keep Enterpret call volume flat regardless of frequency | Tech answers Q1; Enterpret notes |
| A5 | First write-back target is about a two to three week slice once credentials exist; a second system costs less | Tech answers Q5 |
| A6 | Most Gainsight configurations allow custom home-page links | Tech answers Q4 |
| A7 | Enterpret live feed lands within 72 hours, often the same day | Notes 15 Oct L362 |
| A8 | Current model confidence is about 90% | Notes 15 Oct L370 |
| A9 | Knowledge library analysis is English only | Notes 15 Oct L386 |
| A10 | Success measures: messages to the VoC leads drop by 50%; a daily interactive feed whose use is tracked | Notes 15 Oct L573, L496 |

## Conflicts with docs/

| Topic | Sources say | docs/ says |
|---|---|---|
| Confidence figure | NAVEX quoted a 90% confidence rate for the current model (Notes 15 Oct L370) | The "90% (plus or minus 5%)" figure is a placeholder (`docs/01-product/open-items.md` #8) |
| Org chart source | Needs agreement: Entra manager attribute or HR feed (Tech answers Q3) | TEAM scope uses the org chart with no source named, and no open item (`docs/01-product/roles-and-access.md`, Data scopes) |
| Enterpret questions | Five open questions (Enterpret notes) | Open item #18 lists only the request ceiling and the service account seat |
