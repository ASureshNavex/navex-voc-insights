"""Amazon Bedrock AgentCore Runtime entry point for the Account Scoring Agent."""

from functools import lru_cache
from typing import Any

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from account_scoring_agent.core.bedrock import BedrockSummariser
from account_scoring_agent.core.config import get_settings
from account_scoring_agent.core.telemetry import configure_logging
from account_scoring_agent.domain.scoring import ThresholdRuleSet
from account_scoring_agent.graphs.account_scoring.graph import run_scoring
from account_scoring_agent.graphs.account_scoring.nodes import Dependencies
from account_scoring_agent.tools.events import EventBridgePublisher
from account_scoring_agent.tools.serving_store import SqlServingStore

app = BedrockAgentCoreApp()


@lru_cache
def _dependencies() -> Dependencies:
    settings = get_settings()
    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    return Dependencies(
        store=SqlServingStore(async_sessionmaker(engine, expire_on_commit=False)),
        rules=ThresholdRuleSet.load(settings.rule_set_path),
        summariser=BedrockSummariser(settings),
        events=EventBridgePublisher(settings.event_bus_name, settings.aws_region),
        confirm_runs=settings.confirm_runs,
        driver_verbatims_per_theme=settings.driver_verbatims_per_theme,
        summary_concurrency=settings.summary_concurrency,
    )


@app.entrypoint
async def invoke(payload: dict[str, Any]) -> dict[str, Any]:
    """Payload: {"run_id": "<uuid>"}, sent by the ingestion task once evidence is staged."""
    run_id = str(payload["run_id"])
    state = await run_scoring(_dependencies(), run_id)
    return {
        "run_id": run_id,
        "published": state.get("published", False),
        "accounts": len(state.get("scored", [])),
        "status_changes": state.get("status_changes", 0),
    }


if __name__ == "__main__":
    configure_logging()
    app.run()
