"""Enterpret through its MCP API. Code chooses the tools; no model is involved."""

from typing import Any

import httpx2
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from ingestion.models import AccountFeedback, TaxonomyTheme

TOOL_TIMEOUT_SECONDS = 120.0
_TIMEOUT = httpx2.Timeout(TOOL_TIMEOUT_SECONDS, connect=10.0)


class EnterpretError(RuntimeError):
    pass


class EnterpretFeedbackSource:
    def __init__(self, url: str, token: str) -> None:
        self._url = url
        self._headers = {"Authorization": f"Bearer {token}"}

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        async with (
            httpx2.AsyncClient(headers=self._headers, timeout=_TIMEOUT) as http_client,
            streamable_http_client(self._url, http_client=http_client) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()
            result = await session.call_tool(
                name, arguments, read_timeout_seconds=TOOL_TIMEOUT_SECONDS
            )
        if getattr(result, "is_error", False):
            raise EnterpretError(f"Enterpret tool {name} returned an error.")
        return getattr(result, "structured_content", None) or {}

    async def fetch_taxonomy(self) -> list[TaxonomyTheme]:
        # Unit ING-02: map `resolve_taxonomy_scope` to TaxonomyTheme once the probe confirms fields.
        raise NotImplementedError("ING-02")

    async def fetch_feedback(self, window_days: int) -> list[AccountFeedback]:
        # Unit ING-02: `run_graph_query` for theme and sentiment counts per account, then
        # `find_user_quote` for driver verbatims, mapped to AccountFeedback.
        raise NotImplementedError("ING-02")
