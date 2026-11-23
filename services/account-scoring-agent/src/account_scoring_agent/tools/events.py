import asyncio
import json

import boto3
from botocore.config import Config


class EventBridgePublisher:
    """Announces a published run. An EventBridge rule starts the notification task from it."""

    def __init__(self, bus_name: str, region: str) -> None:
        self._bus_name = bus_name
        self._client = boto3.client(
            "events", region_name=region, config=Config(connect_timeout=3, read_timeout=10)
        )

    async def run_published(self, run_id: str, status_changes: int) -> None:
        entry = {
            "Source": "voc.account-scoring-agent",
            "DetailType": "run.published",
            "Detail": json.dumps({"run_id": run_id, "status_changes": status_changes}),
            "EventBusName": self._bus_name,
        }
        await asyncio.to_thread(self._client.put_events, Entries=[entry])
