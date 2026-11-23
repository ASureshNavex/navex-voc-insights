"""The deterministic steps that run before scoring: pull, mask, match and stage."""

import logging
from dataclasses import dataclass

from ingestion.masking import mask_personal_details
from ingestion.matching import match_feedback
from ingestion.models import AccountFeedback, IngestionResult
from ingestion.ports import AccountSource, FeedbackSource, ScoringAgent, StagingStore

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Dependencies:
    accounts: AccountSource
    feedback: FeedbackSource
    store: StagingStore
    scoring_agent: ScoringAgent
    window_days: int


def _masked(item: AccountFeedback) -> AccountFeedback:
    verbatims = [
        verbatim.model_copy(update={"text": mask_personal_details(verbatim.text)})
        for verbatim in item.verbatims
    ]
    return item.model_copy(update={"verbatims": verbatims})


async def run_ingestion(deps: Dependencies) -> IngestionResult | None:
    run_id = await deps.store.start_run()
    if run_id is None:
        logger.info("A run is already active; nothing to do.")
        return None
    try:
        accounts = await deps.accounts.fetch_accounts()
        themes = await deps.feedback.fetch_taxonomy()
        feedback = await deps.feedback.fetch_feedback(deps.window_days)
        matched, unmatched_records = match_feedback(accounts, feedback)
        staged = [_masked(item) for item in matched]
        await deps.store.stage(run_id, accounts, themes, staged, unmatched_records)
    except Exception as exc:
        # The published run stays in place; readers never see a partial run.
        await deps.store.fail_run(run_id, f"Ingestion failed: {type(exc).__name__}")
        raise
    await deps.scoring_agent.start(run_id)
    return IngestionResult(
        run_id=run_id,
        accounts=len(accounts),
        matched=len(staged),
        unmatched_records=unmatched_records,
    )
