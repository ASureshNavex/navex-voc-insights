import asyncio
import json

import boto3
from botocore.config import Config


class AgentCoreScoringAgent:
    """Starts the Account Scoring Agent on Amazon Bedrock AgentCore Runtime for one run."""

    def __init__(self, runtime_arn: str, region: str) -> None:
        self._runtime_arn = runtime_arn
        self._client = boto3.client(
            "bedrock-agentcore",
            region_name=region,
            config=Config(connect_timeout=5, read_timeout=900, retries={"max_attempts": 2}),
        )

    async def start(self, run_id: str) -> None:
        await asyncio.to_thread(
            self._client.invoke_agent_runtime,
            agentRuntimeArn=self._runtime_arn,
            # One session per run keeps a retried invocation on the same session.
            runtimeSessionId=f"account-scoring-{run_id}",
            contentType="application/json",
            payload=json.dumps({"run_id": run_id}).encode(),
        )
