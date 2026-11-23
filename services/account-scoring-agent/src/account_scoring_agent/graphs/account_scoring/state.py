from typing import TypedDict

from account_scoring_agent.domain.models import AccountInput, ScoredAccount


class ScoringState(TypedDict, total=False):
    run_id: str
    accounts: list[AccountInput]
    scored: list[ScoredAccount]
    status_changes: int
    published: bool
