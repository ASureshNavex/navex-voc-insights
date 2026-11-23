# Infrastructure

NAVEX IT provisions every resource in NAVEX's four standard shared AWS environments: DEV, QA, Staging and Prod. This repository holds no infrastructure code. This file is the contract between the code and the environment.

The inventory, sizing, provisioning checklist and cost are in the workbook `NAVEX_VoC_Cost_and_Infrastructure_by_Environment.xlsx`. Note that the workbook and the design diagrams predate the split of the background work into the ingestion task and the Account Scoring Agent, and still name a single "Refresh Agent".

## Deployable units

| Unit | Image or artefact | Runs on | Started by |
|---|---|---|---|
| Web app | `apps/web/dist` | S3 behind CloudFront with WAF | User |
| Experience API | `services/experience-api/Dockerfile` | ECS Fargate behind the load balancer; health check `/health`, readiness `/ready` | Always on |
| Ingestion task | `services/ingestion/Dockerfile` | ECS Fargate task | EventBridge Scheduler |
| Account Scoring Agent | `services/account-scoring-agent/Dockerfile` | Amazon Bedrock AgentCore Runtime, port 8080 | Ingestion task, `InvokeAgentRuntime` |
| Notification task | `services/notifications/Dockerfile` | ECS Fargate task | EventBridge rule on `run.published`; Scheduler for digests |
| Database migrations | `packages/voc-data/alembic` | Run in the deploy pipeline before the API rolls out | Deploy |

Build every image from the repository root, for example `docker build -f services/experience-api/Dockerfile .`. Images run as a non-root user.

## Configuration

Each service reads environment variables; the names are in its `.env.example`. Secrets come from AWS Secrets Manager, never from the image or the repository.

| Secret | Used by |
|---|---|
| PostgreSQL connection string | All four services |
| Snowflake private key | Ingestion task |
| Enterpret MCP token for `voc-insights@navex.com` | Ingestion task |

## IAM, by unit

| Unit | Needs |
|---|---|
| Experience API | RDS connect; S3 presign on the documents bucket; EventBridge put for digest sends |
| Ingestion task | RDS connect; the two secrets; `bedrock-agentcore:InvokeAgentRuntime` on the agent; PrivateLink route to Snowflake; outbound HTTPS to Enterpret |
| Account Scoring Agent | RDS connect; `bedrock:InvokeModel` on the approved model; EventBridge put |
| Notification task | RDS connect; SES send from `voc-insights@navex.com` |

## Events

| Event | Source | Detail | Consumer |
|---|---|---|---|
| `run.published` | `voc.account-scoring-agent` | `run_id`, `status_changes` | Rule that starts the notification task with `alerts --run-id` |

## Telemetry

Services emit OpenTelemetry over OTLP using the standard `OTEL_EXPORTER_OTLP_*` variables, pointed at NAVEX's Dynatrace tenant. Logs are JSON on standard output.
