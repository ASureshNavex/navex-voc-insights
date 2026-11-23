# 10 Domain model: feedback entities, account fields, product domains
Sources: NAVEX Domain Model July 2026.pdf (p.1 "Step 1 -- Metrics we ingest"); NAVEX RYGG Account Model.pdf/.docx (June 2026 v3, Glossary); skills step-1a..1d, step-2, step-3, domain-detail-reports, weekly-voc-html-report (Friction_Report_Scoring_HTML_Skills); navex-qbr-factbase skill (FactBase zip).

Note: despite its file name, "NAVEX Domain Model July 2026.pdf" is the product-domain scoring method ("VoC Product Domain Scoring -- How It Works"). Its scoring content is in `10a-product-domain-scoring.md`. The entity model below is assembled from the Cypher the skills run against Enterpret.

## Already in docs/ (read there, not here)

- Application data model (account, account_rating, account_theme, theme, verbatim_ref, weekly_snapshot ...): `docs/02-architecture/lld.md` "3.2 Data dictionary".
- Terms (Account, ARR, CXM, AE, Exec sponsor, Super product family, Taxonomy, Theme, NPS): `docs/01-product/glossary.md`.
- Enterpret and Snowflake interface calls: `docs/02-architecture/lld.md` "4.2 Enterpret", "4.3 Snowflake".

## Upstream data flow (Domain Model p.1; step-3 skill)

    Snowflake (support cases, CSAT, NPS, issues, product ideas, account master)
       -> Enterpret Wisdom Knowledge Graph (AI tags: product domain L1/L3, theme, sentiment)
       -> skills query the graph (Cypher via Enterpret connector; results in `rows_v2`)
       -> JSON cohort files -> standalone HTML reports
    Side inputs: Exec_Outreach_mapping.xlsx (exec sponsor), Aha! (roadmap, ideas),
                 Klue (competitors, Fact Base only), UG/NCC notes and Go-To-Green (Fact Base only)

## Feedback sources

| Source | `nli.source` value | Captures | Scale (Domain Model p.1) | Domain rating | Account rules |
|---|---|---|---|---|---|
| Support Cases | `Snowflake-Support Cases` | Customer-submitted tickets; primary complaint signal | Highest | Yes, primary | Only source for AR3/AY3 recency |
| CSAT Survey Results | `Snowflake-CSAT Survey Results` | Post-interaction satisfaction | Moderate | Yes | AY4 (guide only, see 11) |
| NPS Survey Results | `Snowflake-NPS Survey Results` | Relationship sentiment | Lower | Yes | Context only (NPS column) |
| Issues | `Snowflake-Issues` | Logged bugs/defects; Salesforce ERC record; type Red / Yellow / Escalation | Low | Context only | Issue status (step-2) |
| Product Ideas | `Snowflake-Product Ideas` | Feature requests; Aha! idea URL | Low | Context only | - |

Record counts grow every run; the PDF gives relative scale, not totals (Domain Model p.1).

## Enterpret graph entities (skills Cypher)

| Node | Attributes used | Notes |
|---|---|---|
| NaturalLanguageInteraction (`nli`) | `record_id`, `record_timestamp`, `source`, `text`, source-specific `snowflake_*` fields | One feedback record; counted with `COUNT(DISTINCT nli.record_id)` |
| FeedbackInsight (`fi`) | `content` | AI summary of the record. Churn phrases are matched here; summaries are grounded in it |
| CustomerFeedbackTags (`cft`) | - | Tag bundle linking a record to themes and taxonomy |
| Theme (`t`) | `name`, `category_enum` (COMPLAINT, PRAISE, IMPROVEMENT, HELP), `type` | Complaint = `category_enum CONTAINS 'COMPLAINT' AND type != 'MISC'` |
| L1 | `name`, `type` | Product-domain level; filtered by `name CONTAINS <keyword>`; `type != 'MISC'` |
| L3 | `name`, `type` | Detailed topic; `name = 'General'` skipped in chips |
| SentimentPrediction (`sp`) | `label` | Negative = `label = 'Negative'` (account skills) |
| Account (`acc`) | `record_id`, `snowflake_accounts_*` | Account master mirrored from Snowflake |

Relationships:

    (nli)-[:SUMMARIZED_BY]->(fi)-[:HAS_TAGS]->(cft)-[:HAS_THEME]->(t:Theme)
    (cft)-[:BELONGS_TO_L1]->(l1:L1)      (cft)-[:BELONGS_TO_L3]->(l3:L3)
    (fi)-[:HAS_SENTIMENT]->(sp:SentimentPrediction)
    (nli)-[:PROVIDED_BY_ACCOUNT]->(acc:Account)

A record has exactly one L1 (detail skill, Performance/Reliability note). An L2 level exists (product brief output shows L2 headers) but no skill queries it.

## Account fields (prefix `acc.snowflake_accounts_`)

| Field | Meaning | Format / values |
|---|---|---|
| `account_name` | Account name; the join key in every skill query and between JSON files | Text; match by name, not ID |
| `total_asset_arr` | ARR; scoring filter | Numeric; 0 or null -> account excluded (step-1a) |
| `customer_experience_manager` | CXM | Text |
| `customer_success_manager` | CSM | Queried in step-1a, not output |
| `account_owner` | Account Executive | Text (step-3 enrichment) |
| `account_segment` | Segment | AMER: `Enterprise`, `MidMarket`, `SMB`; EAPJ: `Japan`, `DACH`, `UK&I`, `N&W Europe`, `ROW`. Case-sensitive |
| `account_region` | Region | `AMER`, `EMEA/APJ` |
| `active_super_product_families` | SPF | Semicolon-delimited; values seen: 3P Risk Management, Compliance Training, Disclosure Management, Incident Management, IRM, NAVEX One, Policy Management, RCM, WhistleB, Other |
| `nearest_future_contract_end` | Next renewal | `"YYYY-MM-DD HH:MM:SS +0000 UTC"`; first 10 chars, shown `Mon DD, YYYY` |
| `executive_sponsor` | Does not exist | Exec sponsor comes only from Exec_Outreach_mapping.xlsx: col 2 ACCOUNT_NAME, col 4 ELT_OWNER; names normalized (lowercase, alnum, single spaces); blank or "(blank)" skipped; first occurrence wins (step-3) |

## Record-level fields

| Area | Field (on `nli`) | Notes |
|---|---|---|
| Issues | `snowflake_issues_issue_status_s__sl` | Status, string list; may be blank on older issues |
| Issues | `snowflake_issues_ercid__sl`, `..._issue_type_s__sl`, `..._date_reported_s__sl`, `..._erccreatedat__nl` | ERC id, type (Red / Yellow / Escalation), date reported, created epoch seconds |
| Issues | (none) | No issue closed-date field exists; "last issue activity" = max `record_timestamp` (step-2) |
| NPS | `snowflake_nps_survey_results_net_promotor_category_s__sl` | `Promotor` / `Passive` / `Detractor`; display "Promoter". Date = `record_timestamp`; `..._feedback_date_s` does not exist |
| Links | `snowflake_support_cases_salesforce_link_s`, `snowflake_issues_salesforce_link_s`, `snowflake_product_ideas_salesforce_link_s`, `snowflake_product_ideas_idea_url_s` | Use whichever is non-null; Aha! URL is the idea fallback (validated June 2026) |
| Cases | `snowflake_support_cases_subject_s` | Case subject, used as one-line description |

Issue status values (step-2; Decided 2026-10-23 for Health Data Action):

| Status | Counts as open |
|---|---|
| Open - Unresolved | Yes |
| Open - Health Data Action | Yes |
| Closed - Resolved / Closed - Unresolved / Closed - Health Data Action / Closed - Unresponsive Health Data / Duplicate | No |
| blank | Only if issue activity within 90 days of run date |

NPS bands (RYGG guide Glossary): Promoter 9-10, Passive 7-8, Detractor 0-6. Most recent response, all-time.

## Product domains (14)

Display name and L1 keyword from weekly-voc-html-report; slug from domain-detail-reports; tier is the skill's static table (re-classified per run, see 10a); Fact Base column from navex-qbr-factbase.

| # | Display name | L1 filter keyword | File slug | Tier | Fact Base domain (Aha! Owning Product) |
|---|---|---|---|---|---|
| 1 | EthicsPoint Incident Management | EthicsPoint | EthicsPoint | High | EPIM (EthicsPoint) |
| 2 | Policy Management (PolicyTech) | PolicyTech | PolicyTech | Mid | PolicyTech (PolicyTech) |
| 3 | Disclosure Management | Disclosure Management | Disclosure | Low | Disclosure Management |
| 4 | Compliance Training: Tech (NAVEXEngage) | Compliance Training: Tech | CT-Tech | Mid | NAVEXEngage (both L1s merged) |
| 5 | Compliance Training: Content (NAVEXEngage) | Compliance Training: Content | CT-Content | Low | NAVEXEngage |
| 6 | Third-Party Risk Management (RiskRate) | RiskRate | RiskRate | Low | RiskRate |
| 7 | Integrated Risk Management (IRM/LockPath) | LockPath | IRM-LockPath | Low | IRM |
| 8 | NAVEX One Platform | NAVEX One | NAVEX-One | High | NAVEXOne Platform (NAVEX One; L1 "NAVEX One Platform") |
| 9 | Insights and Analytics (GRC Insights) | GRC Insights | GRC-Insights | Low | GRC Insights |
| 10 | Regulatory Change Management | Regulatory Change | Reg-Change | Low | - |
| 11 | WhistleB | WhistleB | WhistleB | Low | WhistleB |
| 12 | Performance / Reliability | `Performance` OR `Reliability` (two L1s) | Performance-Reliability | High | - (cross-product) |
| 13 | Usability | Usability | Usability | High | - (cross-product) |
| 14 | Nira (NCAv2) | Nira | Nira | Low | - (new; expected Gray ~8 weeks after launch) |

Other L1 names appear in account taxonomy chips (for example "Contact Center And Telecom") but are not scored domains.

Aha! workspaces searched for roadmap work: N1, NE, NECON, PT, EP, IRM, GRCI, RR, DM, WB, COMPANY (weekly skill). Initiative IDs carry a product prefix, for example `GRCI-S-125`, `RR-N-80`, `EP-582` (Fact Base skill). Aha! idea workflow statuses: Future Consideration, In Development, Planned, Launched, Needs Review.

## Conflicts with docs/

- Join key: `docs/01-product/glossary.md` "Account" and `docs/02-architecture/lld.md` "3.2" (`sfdc_account_id`) key accounts by Salesforce account ID; every skill joins on `acc.snowflake_accounts_account_name` and the exec map on a normalized name (step-1a Phase 2, step-3 Step 3).
- Exec sponsor: `docs/01-product/open-items.md` item 10 expects it in the Snowflake field mapping; step-3 states `snowflake_accounts_executive_sponsor` does not exist and the xlsx is the only source.
- Region: docs give no values; sources use `AMER` and `EMEA/APJ` for accounts, while the weekly skill expects AMER / EMEA / APAC (see 13).

## Open questions

- Domain count: Domain Model p.1 says thirteen domains; the weekly skill and the Sept 2026 Domains output have fourteen (Nira added).
- Issues source match: step-2 filters `nli.source CONTAINS 'issues'` and uses `__sl`-suffixed account fields; other skills use `Snowflake-Issues` and unsuffixed fields. Which form the graph needs is not stated.
- Mapping from super product family (account level) to the 14 product domains (L1) is not given.
- Fact Base 10th domain "Content (Training/CoC/Awareness)" is not built; scoping owner to confirm (Fact Base skill catalog).
- Enterpret record link: detail skill uses `/navex/feedback/{record_id}`, weekly skill Step 3B uses `/navex/records/{record_id}`.
