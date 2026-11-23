# Cost and sizing

Sources: `NAVEX VoC - Technical Architecture and Sizing.pptx` (Arch deck, 17 Nov 2026: slides 15-19); `NAVEX_VoC_Cost_and_Infrastructure_by_Environment.xlsx` (Cost xlsx, 18 Nov 2026: Cost and Inputs sheets).

All money is USD, average monthly unless stated; annual = 12 x average month. Both sources use AWS list prices in us-east-1 and call themselves planning estimates.

## Already in docs/

`docs/02-architecture/overview.md` "Environments" and `infra/README.md` point to the Cost xlsx and restate none of it. Nothing below is in docs/.

## Sizing basis (Arch deck slide 15)

| Measure | MVP | Target | Drives |
|---|---|---|---|
| Named users | 120 | 150 | Sign-in and API sizing |
| VoC admins | under 10 | under 10 | Admin and approval load |
| Daily active users, average | 50 | 70 | API request rate |
| Accounts scored per run | 150 | 150 | Refresh Agent duration |
| Refresh runs a day | 3 | 3 | Task hours, Snowflake and Enterpret calls |
| Account views a day | 500 | 700 | Reads of the published run |
| Peak concurrent API requests | 15 | 20 | API task count |
| Summaries generated a month | 2,700 | 2,700 | Bedrock |
| Account briefs a month | 300 | 450 | Bedrock |
| Research sessions a month | 0 | 200 | AgentCore Runtime sessions |
| Knowledge Hub uploads a month | 20 | 40 | S3 and scan volume |
| Knowledge Hub storage | 1 GB | 5 GB | S3 and Knowledge Bases index |

Workbook adds: about 30,000 records in RDS overall; 150 accounts = three 50-account scorecards (Cost xlsx, Cost and Inputs sheets).

## Cost xlsx: budget by environment (Cost sheet, 18 Nov)

| Item | DEV | QA | Staging | Prod | Shared | Total MVP | Total P1+P2 run rate |
|---|---|---|---|---|---|---|---|
| ECS Fargate: API and Notification | 5 | 15 | 15 | 30 (P1+P2: 58) | 0 | 65 | 93 |
| AgentCore Runtime agents | 0 (1) | 0 (1) | 1 (2) | 1 (6) | 0 | 2 | 10 |
| RDS PostgreSQL | 26 | 26 | 26 | 56 (62) | 0 | 134 | 140 |
| Logs, secrets, S3, file scanning | 2 | 2 | 3 | 6 (12) | 0 | 13 | 19 |
| NAVEX shared infrastructure (network, edge, ALB, cluster, observability) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| AWS subtotal | 33 (34) | 43 (44) | 45 (46) | 93 (138) | 0 | 214 | 262 |
| Snowflake warehouse credits | 4 | 4 | 8 | 32 (72) | 0 | 48 | 88 |
| Enterpret MCP access and seat | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Amazon Bedrock | 5 | 5 | 10 (15) | 21.15 (85.65) | 0 | 41.15 | 110.65 |
| Dynatrace (existing tenant) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Service account M365 licence | 0 | 0 | 0 | 4 | 4 | 8 | 8 |
| GitHub and Actions | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Total monthly | 42 (43) | 52 (53) | 63 (69) | 150.15 (299.65) | 4 | 311.15 | 468.65 |
| Total annual | 504 | 624 | 756 | 1,801.80 | 48 | 3,733.80 | 5,623.80 |

Parentheses = Phase 1 and Phase 2 run rate. Change from MVP: +157.50 a month, +1,890 a year. Zero lines are Assumed (shared infra with no chargeback; Enterpret within subscription; GitHub within plan).

### Cost xlsx inputs (Inputs sheet)

| Input | MVP | P1+P2 | Basis |
|---|---|---|---|
| Snowflake rate per credit | 4.00 | 4.00 | Business Critical list rate, AWS US, Assumed; replace with contracted rate |
| Snowflake credits a month DEV/QA/Staging/Prod | 1/1/2/8 | 1/1/2/18 | X-Small, 60 s auto-suspend; P1+P2 adds domain and Fact Base reads |
| Share of accounts whose inputs change per run | 0.05 | 0.05 | Summary regenerated only on change |
| Cost per summary | 0.018 | 0.018 | ~4,000 input + 400 output tokens, Assumed |
| Briefs a month x cost | 300 x 0.03 | 450 x 0.03 | ~6,000 input + 800 output tokens, Assumed |
| Research sessions x cost | 0 | 200 x 0.25 | Insights agent, Assumed |
| Fact Base narratives | 0 | 10 a month | Phase 2 |
| Bedrock Prod total | 21.15 | 85.65 | Sum of the above (30 days, 3 runs, 150 accounts) |
| Refresh runs a day | 3 | 3 | "Pending NAVEX's cost confirmation" |

## Arch deck: cost by environment (slides 17-19, 17 Nov)

| Component | Dev | UAT | Prod | Shared non-prod | Monthly | Annual |
|---|---|---|---|---|---|---|
| ECS Fargate API + Notification | 11 | 59 | 145 | - | | |
| AgentCore Runtime (3 agents) | 2 | 4 | 23 | - | | |
| RDS compute and storage | 26 | 53 | 211 | - | | |
| ALB and WAF | - | - | 33 | 33 | | |
| NAT, PrivateLink, interface endpoints | - | - | 70 | 41 | | |
| CloudWatch, Secrets, S3, GuardDuty scan, S3 Vectors | 4 | 6 | 20 | - | | |
| AWS infrastructure subtotal | 43 | 122 | 502 | 74 | 741 | 8,892 |
| Snowflake and Enterpret access | 10 | 30 | 189 | - | 229 | 2,748 |
| Bedrock, budget cap | 20 | 50 | 230 | - | 300 | 3,600 |
| Dynatrace, existing tenant | 0 | 0 | 0 | - | 0 | 0 |
| Service account M365 | 0 | 0 | 4 | 4 | 8 | 96 |
| Total | 73 | 202 | 925 | 78 | 1,278 | 15,336 |

Covers the full roadmap. During MVP the usage lines run lower: Snowflake and Enterpret 149 a month, Bedrock 100 a month (slide 19).

### Data access detail (slide 18, Prod)

| Item | Basis | Volume a month | Rate | USD |
|---|---|---|---|---|
| Snowflake refresh | X-Small, 3 runs x 10 min incl. auto-suspend | 15 credits | 4.00 | 60 |
| Snowflake evidence on demand | X-Small, 1 active hour per working day | 22 credits | 4.00 | 88 |
| Snowflake P1 and P2 evidence | Domain and Fact Base reads | 20 credits | 4.00 | 80 |
| Snowflake storage | Reads existing tables; stores nothing new | 0 | | 0 |
| PrivateLink endpoint | 1 endpoint, 2 AZ | 1,460 h | 0.01/h/AZ | in infra |
| PrivateLink data | 150 accounts per run plus drill-down | 5 GB | 0.01/GB | under 1 |
| Enterpret MCP refresh | 21 queries per run | 1,900 calls | subscription | 0 incremental |
| Enterpret evidence | Verbatims served from PostgreSQL | 0 calls | | 0 |
| Total | | | | 229 / month, 2,748 / year |

Cost behaviour: Snowflake cost follows warehouse active time; aggregation runs in Enterpret and scoring in the agent, so the warehouse serves short reads.

## Conflicts with docs/

None: docs/ holds no cost or sizing figures and names the Cost xlsx as the reference. Source-to-source conflicts a reader must know:

| Topic | Arch deck (17 Nov) | Cost xlsx (18 Nov) |
|---|---|---|
| Total | 1,278 / month, 15,336 / year (full roadmap) | 311.15 MVP, 468.65 P1+P2 / month **Resolved 2026-11-19: the workbook, 311 to 469 a month (adr/0003).** |
| Why | Dedicated Prod network, ALB, NAT charged; larger tasks; Bedrock as budget cap | Shared NAVEX infra at 0; minimal sizes; Bedrock computed from drivers |
| Prod RDS | db.t4g.large Multi-AZ 100 GB, 211 | db.t4g.small Multi-AZ 20 GB, 56 |
| Prod Snowflake | 37 credits MVP, 57 with P1+P2 | 8 credits MVP, 18 P1+P2 |

The workbook is the later document and the one docs/ cites.

## Open questions

- NAVEX contracted Snowflake credit rate and edition.
- Whether NAVEX charges back shared infrastructure (workbook line is 0 "enter a chargeback here").
- Whether a paid Enterpret seat is needed for the service account.
- Confirmation of 3 refresh runs a day against cost (Inputs sheet).
