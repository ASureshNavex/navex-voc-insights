# AWS infrastructure and environments

Sources: `NAVEX_VoC_Cost_and_Infrastructure_by_Environment.xlsx` (Cost xlsx, 18 Nov 2026: Inventory, Checklist sheets); `NAVEX VoC - Technical Architecture and Sizing.pptx` (Arch deck, 17 Nov 2026: slides 5-10, 16); `NAVEX_VoC_AWS_MVP.drawio`, `NAVEX_VoC_AWS_Target.drawio` (drawio, 4 Nov 2026).

## Already in docs/ (read there, not here)

- Deployable units, secrets, IAM per unit, events, telemetry variables: `infra/README.md`.
- "NAVEX IT provisions every resource; this repository holds no infrastructure code": `infra/README.md` intro; `docs/02-architecture/overview.md` "Environments".
- Deployment narrative (edge, subnets, PrivateLink, NAT): `docs/02-architecture/hld.md` section 8.
- AWS region question: `docs/01-product/open-items.md` item 13.

## Two inventories exist; the workbook is newer

| Aspect | Arch deck (17 Nov) | Cost xlsx (18 Nov), which docs/ follows |
|---|---|---|
| Environments | Dev, UAT, Prod | DEV, QA, Staging, Prod: NAVEX standard shared environments |
| Network | Shared non-production VPC for Dev and UAT; dedicated Prod VPC, 2 AZ, Snowflake PrivateLink (slide 16) | NAVEX standard VPC, subnets, NAT, endpoints, existing in every environment |
| Load balancer | 1 ALB across 2 AZ (slide 8) | Existing shared ALB with a VoC listener rule and target group (To confirm) |
| Sizes | Larger (below) | Minimal, "raised only when monitoring shows sustained load" |
| Region | us-east-1 list prices; region matches Snowflake | Same region as NAVEX's Snowflake; "Region confirmed in writing" is the ready-when |

## Inventory by environment (Cost xlsx, Inventory sheet)

Provisioned by NAVEX IT for every row. "Existing" = NAVEX standard, reused.

| Resource | DEV | QA | Staging | Prod | Provisioning |
|---|---|---|---|---|---|
| AWS account, region, VPC, subnets, NAT, WAF, KMS, CloudWatch, GuardDuty Malware Protection for S3 | Existing | Existing | Existing | Existing | Existing |
| Interface endpoints: Bedrock, Secrets Manager, ECR, CloudWatch Logs | Existing | Existing | Existing | Existing | Existing |
| Snowflake PrivateLink endpoint | Standard where present, else 1 | same | same | same | To confirm |
| Deploy IAM role (GitHub Actions OIDC, no long-lived keys) | 1 | 1 | 1 | 1 | To confirm |
| Domain and ACM certificate | per-env subdomain | per-env subdomain | per-env subdomain | production subdomain | New |
| CloudFront | Standard pattern, VoC origin added | same | same | same | To confirm |
| S3 static site bucket | 1 | 1 | 1 | 1, versioning | New |
| S3 documents bucket (quarantine, review, published prefixes) | 1, scan on | 1, scan on | 1, scan on | 1, scan and versioning | New |
| ECR | 1 repo per image | same | same | same | To confirm |
| ECS cluster on Fargate | Standard cluster or one VoC cluster | same | same | same | To confirm |
| ECS service: Experience API | 0.5 vCPU, 1 GB; 0-1 task, weekday hours | 0.5/1 GB; 1 task | 0.5/1 GB; 1-2 tasks | 0.5/1 GB; 2-4 tasks; scale at 60% CPU; next 1 vCPU, 2 GB | New |
| ECS task: Notification task | 0.5/1 GB on demand | same | 0.5/1 GB per trigger | 0.5/1 GB per trigger | New |
| AgentCore Runtime: Refresh Agent | 1 vCPU, 2 GB/session; on demand | on demand | 1 run a day | 3 runs a day; next 2 vCPU, 4 GB | Existing runtime, new agent |
| Bedrock model access, budget alarm (USD) | 5 | 5 | 10 | quota + 25 for MVP | New |
| EventBridge | Manual trigger | Manual trigger | 1 refresh schedule; digests | 3 refresh schedules; digests; 2 rules | New |
| RDS for PostgreSQL | db.t4g.small, Single-AZ, 20 GB gp3 | same | same | db.t4g.small Multi-AZ, 20 GB, 7-day backups; next db.t4g.medium | New |
| Secrets Manager | 3 VoC secrets | 3 | 3 | 3, rotation schedule | New secrets |
| Email | NAVEX notification service or Amazon SES | same | same | same | To confirm |
| Service account | non-prod account shared by DEV, QA, Staging | shared | shared | prod account | New |
| Dynatrace trace sampling | 1.0 | 1.0 | 0.5 | 0.1 | Existing tenant |
| Snowflake service user | Key pair, read role, X-Small | same | same | X-Small, auto-suspend 60 s | New |
| Enterpret MCP token | non-prod service account | same | same | prod service account | New |
| Gainsight CTA link | Test CTA | Test CTA | Test CTA | VoC CTA | New |

Phase 1 rows: AgentCore Runtime Insights agent (1 vCPU, 2 GB/session; 1, 1, up to 2, up to 5 sessions), AgentCore Gateway (1 per env), AgentCore Identity and Memory (Prod federated with Entra), Bedrock Knowledge Bases with S3 Vectors (1 per env). Phase 2 rows: Fact Base agent (1 vCPU, 2 GB; Prod next 2 vCPU, 4 GB), Klue, Pendo and Aha! credentials (test in lower envs, Secrets Manager in Prod).

Entra rows (app registrations, roles, assignment, Graph, Conditional Access): see `23-identity-and-sso.md`.

## Arch deck sizing (slides 8, 16): Dev, UAT, Prod

| Component | Dev | UAT | Prod |
|---|---|---|---|
| Experience API per task | 1 vCPU, 2 GB | 2 vCPU, 4 GB | 2 vCPU, 4 GB, Graviton |
| API tasks min-max | 0-1, weekday hours | 1-3 | 2-6, target tracking 60% CPU |
| Refresh Agent per session | 1 vCPU, 2 GB | 2 vCPU, 4 GB | 4 vCPU, 8 GB |
| Refresh runs | On demand | 1 a day | 3 a day; monthly domain run from Phase 1 |
| Notification task | 1 vCPU, 2 GB | 1 vCPU, 2 GB | 1 vCPU, 2 GB |
| Insights agent (P1), concurrent sessions | 1 vCPU, 2 GB; 1 | 2 vCPU, 4 GB; up to 3 | 2 vCPU, 4 GB; up to 10 |
| Fact Base agent (P2) | 1 vCPU, 2 GB | 2 vCPU, 4 GB | 4 vCPU, 8 GB |
| RDS | db.t4g.small, Single-AZ, 20 GB | db.t4g.medium, Single-AZ, 50 GB | db.t4g.large, Multi-AZ, 100 GB gp3, autoscale to 500 GB |
| Trace sampling | 1.0 | 0.5 | 0.1 |
| Bedrock | Budget alarm | Budget alarm | Quota and budget alarms |
| Logs retention | | | 14 days (slide 8) |

Prod is "sized once for the full roadmap: 150 named users" (slide 8).

## Network paths (drawio; Arch deck slides 6-7)

| Path | Mechanism |
|---|---|
| Users to app | HTTPS 443 to CloudFront + WAF; S3 static site via OAC |
| Upload | Browser PUT to S3 documents with presigned URL; malware scan on upload |
| API | CloudFront -> internet gateway -> ALB (public subnets) -> Experience API on Fargate (private subnets), container port 8000 |
| Snowflake | PrivateLink endpoint in private subnets (deck: requires Snowflake Business Critical, slide 18) |
| Enterpret, Entra ID (JWKS, Graph), Dynatrace (OTel 443) | NAT gateway egress |
| Regional services | EventBridge Scheduler, CloudWatch, RDS, Bedrock, SES, Secrets Manager; Knowledge Bases in Phase 1 |
| Phase 1 | Agents over MCP -> load balancer -> MCP gateway -> Insights agent; grounds on Knowledge Bases |
| Phase 2 | NAT egress to Klue, Pendo, Aha!; connector tasks on Fargate 1 vCPU, 2 GB per connector (slide 9); "Alternative platform" via port swap |

Accounts: one AWS account per environment, existing NAVEX standard (Cost xlsx Inventory row 1). No account ids recorded here.

## Delivery and readiness (Cost xlsx, Checklist sheet)

- CI/CD (Psiog, New): every PR runs lint, type check, tests, web build, security scans; images built once, pushed to ECR, promoted; migrations run on deploy.
- GitHub environments; higher environments need approval from a named NAVEX reviewer. Main needs PR, one review, passing checks; secret scanning and Dependabot on.
- Snowflake and Enterpret access rows are "Parked" (status of all 20 checklist items: Not started).

## Conflicts with docs/

| # | Topic | Sources | docs/ |
|---|---|---|---|
| 1 | Environment names | Arch deck: Dev, UAT, Prod (slides 5, 16-19) | DEV, QA, Staging, Prod (`overview.md` "Environments", `infra/README.md`), matching Cost xlsx. `hld.md` 8 says "development, test and production" **Resolved 2026-11-19: DEV, QA, Staging, Prod (adr/0001).** |
| 2 | Region | Arch deck and Cost xlsx price in us-east-1; region must match Snowflake | `.env` assumes us-west-2 (`open-items.md` 13); us-west-2 is the AWS SSO portal region in the SSO guide, not a workload decision **Resolved 2026-11-19: us-west-2 (adr/0002).** |
| 3 | Infrastructure as code | Arch deck slide 5: "Infrastructure as code" for Dev, UAT, Prod | "This repository holds no infrastructure code" (`infra/README.md`) |
| 4 | Network ownership | Arch deck: dedicated Prod VPC and own ALB | NAVEX standard shared network (`infra/README.md`), as Cost xlsx |
| 5 | Background compute | Cost xlsx and deck: Refresh Agent on AgentCore; drawio: run control worker on Fargate Spot | Ingestion task on Fargate + Account Scoring Agent on AgentCore (`infra/README.md` "Deployable units"; docs notes the workbook predates this) |
| 6 | Email | Cost xlsx: NAVEX notification service or SES, To confirm | `infra/README.md` IAM: "SES send"; `hld.md` 6: Amazon SES |

## Open questions

- Which AWS region (must equal NAVEX's Snowflake region and edition; PrivateLink needs Business Critical).
- Does an existing NAVEX Snowflake PrivateLink endpoint exist per environment?
- Shared or VoC-specific ECS cluster; shared ALB and CloudFront routing ("Need to check for the CloudFront", Checklist row 6).
- Who owns IaC for VoC resources, given NAVEX IT provisions them.
- Which UAT environment (QA or Staging) hosts NAVEX user acceptance; Staging rows say "UAT testers assigned".
