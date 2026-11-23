# Account Scoring Agent

A LangGraph graph on Amazon Bedrock AgentCore Runtime. It turns the evidence staged by the ingestion task into published ratings.

```text
load_batch -> score -> summarise -> publish
```

| Node | Does | Uses a model |
|---|---|---|
| `load_batch` | Reads the staged evidence for the run | No |
| `score` | Rates each account with the rule set, picks the rule or trigger, ranks themes, selects driver verbatims, confirms status changes | No |
| `summarise` | Writes the friction explanation for red and yellow accounts from a Jinja2 prompt, with Pydantic structured output. Unchanged evidence reuses the previous text. A failed or ungrounded summary is dropped; the rating still publishes | Yes |
| `publish` | Writes the run, switches the published run in one transaction, emits `run.published` | No |

The order is fixed. The model never chooses a step or a tool.

```bash
cp .env.example .env
uv run python -m account_scoring_agent.entrypoint     # serves the AgentCore contract on port 8080
```

```text
src/account_scoring_agent/
├── core/        config, bedrock (model factory), prompt_loader, telemetry
├── domain/      scoring, triggers, theme_ranking, status_confirmation: pure functions
├── graphs/account_scoring/   state, nodes, edges, graph
├── prompts/     every prompt, as .j2 files; shared partials start with an underscore
├── schemas/     prompt context models and structured outputs
├── tools/       ports and adapters: serving store, EventBridge
├── rules/       versioned rule set files
└── entrypoint.py
```

## What is built

The graph, domain rules, prompts, serving store and entry point are built and tested end to end on SQLite with a fake summariser.

| Still to build | Unit |
|---|---|
| Replace `rules/placeholder-v0.yaml` and `friction_score` with NAVEX's rule set | AGT-01 |
| Deploy to AgentCore Runtime in DEV and confirm the model ID | AGT-02 |
| Weekly cut-off handling and the alert evaluation flag | AGT-03 |
| Account brief and leadership weekly brief prompts | AGT-04 |

## Adding a prompt

1. Add the `.j2` file under `prompts/<agent>/`.
2. Add its context model in `schemas/prompt_contexts.py` and its output model in `schemas/outputs.py`.
3. Add it to `CONTEXTS` in `tests/test_prompts.py`. The suite fails until every template has a render test.
