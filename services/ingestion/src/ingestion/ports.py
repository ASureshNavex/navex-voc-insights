from typing import Protocol

from ingestion.models import AccountFeedback, SourceAccount, TaxonomyTheme


class AccountSource(Protocol):
    async def fetch_accounts(self) -> list[SourceAccount]: ...


class FeedbackSource(Protocol):
    async def fetch_taxonomy(self) -> list[TaxonomyTheme]: ...

    async def fetch_feedback(self, window_days: int) -> list[AccountFeedback]: ...


class StagingStore(Protocol):
    async def start_run(self) -> str | None:
        """Open a run and return its ID, or None when another run is still active."""
        ...

    async def stage(
        self,
        run_id: str,
        accounts: list[SourceAccount],
        themes: list[TaxonomyTheme],
        feedback: list[AccountFeedback],
        unmatched_records: int,
    ) -> None: ...

    async def fail_run(self, run_id: str, note: str) -> None: ...


class ScoringAgent(Protocol):
    async def start(self, run_id: str) -> None: ...
