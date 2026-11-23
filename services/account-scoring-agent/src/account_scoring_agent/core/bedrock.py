"""Bedrock model factories. Every analytical call returns a validated Pydantic object."""

from typing import cast

from botocore.config import Config
from langchain_aws import ChatBedrockConverse

from account_scoring_agent.core.config import Settings
from account_scoring_agent.core.prompt_loader import render_prompt
from account_scoring_agent.schemas.outputs import AccountSummary
from account_scoring_agent.schemas.prompt_contexts import AccountSummaryContext


class BedrockSummariser:
    def __init__(self, settings: Settings) -> None:
        model = ChatBedrockConverse(
            model_id=settings.bedrock_model_id,
            region_name=settings.aws_region,
            temperature=0,
            config=Config(
                connect_timeout=5,
                read_timeout=settings.bedrock_timeout_seconds,
                retries={"max_attempts": 3, "mode": "adaptive"},
            ),
        )
        self._model = model.with_structured_output(AccountSummary)

    async def summarise(self, context: AccountSummaryContext) -> AccountSummary:
        messages = [
            ("system", render_prompt("account_scoring/system.j2")),
            ("human", render_prompt("account_scoring/account_summary.j2", context)),
        ]
        return cast(AccountSummary, await self._model.ainvoke(messages))
