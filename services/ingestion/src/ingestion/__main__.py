"""Entry point of the ECS task: `python -m ingestion`. Started by EventBridge Scheduler."""

import asyncio
import logging

import boto3
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ingestion.adapters.agentcore import AgentCoreScoringAgent
from ingestion.adapters.enterpret import EnterpretFeedbackSource
from ingestion.adapters.snowflake import SnowflakeAccountSource
from ingestion.adapters.staging import SqlStagingStore
from ingestion.config import get_settings
from ingestion.pipeline import Dependencies, run_ingestion


def _secret(name: str, region: str) -> str:
    client = boto3.client("secretsmanager", region_name=region)
    return str(client.get_secret_value(SecretId=name)["SecretString"])


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()
    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    deps = Dependencies(
        accounts=SnowflakeAccountSource(
            account=settings.snowflake_account,
            user=settings.snowflake_user,
            private_key=_secret(
                settings.snowflake_private_key_secret, settings.aws_region
            ).encode(),
            warehouse=settings.snowflake_warehouse,
            view=settings.snowflake_account_view,
        ),
        feedback=EnterpretFeedbackSource(
            url=settings.enterpret_mcp_url,
            token=_secret(settings.enterpret_token_secret, settings.aws_region),
        ),
        store=SqlStagingStore(async_sessionmaker(engine, expire_on_commit=False)),
        scoring_agent=AgentCoreScoringAgent(
            settings.scoring_agent_runtime_arn, settings.aws_region
        ),
        window_days=settings.scoring_window_days,
    )
    try:
        result = await run_ingestion(deps)
        logging.getLogger(__name__).info("Ingestion finished: %s", result)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
