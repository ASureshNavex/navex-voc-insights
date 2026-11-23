# Ingestion task

The deterministic steps that run before scoring. An ECS Fargate task started by EventBridge Scheduler.

1. Open a run, unless one is already active.
2. Pull the account master from Snowflake.
3. Pull the taxonomy, theme and sentiment counts, and driver verbatims from Enterpret through its MCP API.
4. Match feedback to accounts on the Salesforce account ID; count what does not match.
5. Mask personal details in verbatims.
6. Stage the evidence in PostgreSQL for the run.
7. Start the Account Scoring Agent on AgentCore Runtime with the run ID.

No model is involved. Code chooses every call.

```bash
cp .env.example .env
uv run python -m ingestion
```

```text
src/ingestion/
├── pipeline.py     the steps, in order
├── ports.py        AccountSource, FeedbackSource, StagingStore, ScoringAgent
├── models.py       shapes that cross the ports
├── masking.py      personal detail masking
├── matching.py     feedback to account matching
└── adapters/       Snowflake, Enterpret (MCP), PostgreSQL staging, AgentCore invoke
```

## What is built

The pipeline, masking, matching, the staging store and the AgentCore start call are built and tested on fakes.

| Still to build | Unit |
|---|---|
| `EnterpretFeedbackSource.fetch_taxonomy` and `fetch_feedback`: map the MCP tool results once the probe confirms field names | ING-02 |
| Confirm the Snowflake view and the column names in `adapters/snowflake.py` | ING-01 |
| Retry with backoff on source calls; source health records | ING-03 |
