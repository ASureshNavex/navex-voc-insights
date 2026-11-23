from typing import Literal

from account_scoring_agent.graphs.account_scoring.state import ScoringState


def after_load(state: ScoringState) -> Literal["score", "fail_empty"]:
    return "score" if state.get("accounts") else "fail_empty"
