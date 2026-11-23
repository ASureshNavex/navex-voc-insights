from typing import Protocol

from account_scoring_agent.domain.models import AccountInput, ScoredAccount
from account_scoring_agent.schemas.outputs import AccountSummary
from account_scoring_agent.schemas.prompt_contexts import AccountSummaryContext


class ServingStore(Protocol):
    async def load_batch(self, run_id: str) -> list[AccountInput]:
        """The evidence the ingestion task staged for this run."""
        ...

    async def cached_explanation(self, account_id: str, evidence_hash: str) -> str | None:
        """The explanation already written from identical evidence, if there is one."""
        ...

    async def publish(self, run_id: str, scored: list[ScoredAccount]) -> None:
        """Write the run and switch the published run in one transaction."""
        ...

    async def fail_run(self, run_id: str, note: str) -> None: ...


class Summariser(Protocol):
    async def summarise(self, context: AccountSummaryContext) -> AccountSummary: ...


class EventPublisher(Protocol):
    async def run_published(self, run_id: str, status_changes: int) -> None: ...
