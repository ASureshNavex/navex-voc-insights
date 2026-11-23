"""Graph nodes. Each takes the state, does one job through its ports, and returns the change."""

import asyncio
import hashlib
import logging
from dataclasses import dataclass, replace

from voc_data.enums import Rating

from account_scoring_agent.domain.models import AccountInput, ScoredAccount
from account_scoring_agent.domain.scoring import RuleSet
from account_scoring_agent.domain.status_confirmation import confirm_status
from account_scoring_agent.domain.theme_ranking import driver_verbatims, rank_themes
from account_scoring_agent.domain.triggers import trigger_for
from account_scoring_agent.graphs.account_scoring.state import ScoringState
from account_scoring_agent.schemas.prompt_contexts import (
    AccountSummaryContext,
    EvidenceItem,
    ThemeLine,
)
from account_scoring_agent.tools.ports import EventPublisher, ServingStore, Summariser

logger = logging.getLogger(__name__)

_RATING_LABEL = {Rating.RED: "Red", Rating.YELLOW: "Yellow", Rating.GREEN: "Green"}


@dataclass(frozen=True, slots=True)
class Dependencies:
    store: ServingStore
    rules: RuleSet
    summariser: Summariser
    events: EventPublisher
    confirm_runs: int = 2
    driver_verbatims_per_theme: int = 2
    summary_concurrency: int = 4


def _summary_context(item: ScoredAccount) -> AccountSummaryContext:
    previous = item.account.previous_week_status
    return AccountSummaryContext(
        account_name=item.account.name,
        rating=_RATING_LABEL[item.decision.rating],
        previous_rating=_RATING_LABEL[previous] if previous else None,
        rule_text=item.trigger.text,
        products=list(item.account.products),
        themes=[ThemeLine(name=t.name, volume=t.volume, negative_volume=t.negative_volume)
                for t in item.themes],
        evidence=[EvidenceItem(id=v.verbatim_id, source=v.source,
                               date=v.feedback_date.isoformat(), text=v.text)
                  for v in item.drivers],
    )  # fmt: skip


def _evidence_hash(context: AccountSummaryContext) -> str:
    return hashlib.sha256(context.model_dump_json().encode()).hexdigest()


class Nodes:
    def __init__(self, deps: Dependencies) -> None:
        self._deps = deps

    async def load_batch(self, state: ScoringState) -> ScoringState:
        return {"accounts": await self._deps.store.load_batch(state["run_id"])}

    async def fail_empty(self, state: ScoringState) -> ScoringState:
        await self._deps.store.fail_run(state["run_id"], "No staged accounts for this run.")
        return {"published": False}

    def _score(self, account: AccountInput) -> ScoredAccount:
        deps = self._deps
        decision = deps.rules.rate(account)
        themes = rank_themes(account.theme_counts)
        state, change = confirm_status(
            account.account_id, account.state, decision.rating, deps.confirm_runs
        )
        return ScoredAccount(
            account=account,
            decision=decision,
            trigger=trigger_for(
                decision.rating, account.previous_week_status, account.churn_language
            ),
            themes=themes,
            drivers=driver_verbatims(themes, account.verbatims, deps.driver_verbatims_per_theme),
            state=state,
            change=change,
        )

    async def score(self, state: ScoringState) -> ScoringState:
        scored = [self._score(account) for account in state["accounts"]]
        return {"scored": scored, "status_changes": sum(1 for s in scored if s.change)}

    async def _explain(self, item: ScoredAccount, limit: asyncio.Semaphore) -> ScoredAccount:
        if item.decision.rating is Rating.GREEN or not item.drivers:
            return item
        context = _summary_context(item)
        evidence_hash = _evidence_hash(context)
        cached = await self._deps.store.cached_explanation(item.account.account_id, evidence_hash)
        if cached:
            return replace(item, explanation=cached, explanation_hash=evidence_hash)
        try:
            async with limit:
                summary = await self._deps.summariser.summarise(context)
        except Exception:
            # The rating stands without its explanation; the page says it is unavailable.
            logger.exception("Summary failed for account %s", item.account.account_id)
            return item
        known = {v.verbatim_id for v in item.drivers}
        if not set(summary.cited_verbatim_ids) <= known:
            logger.warning("Summary cited unknown evidence for %s", item.account.account_id)
            return item
        return replace(item, explanation=summary.explanation, explanation_hash=evidence_hash)

    async def summarise(self, state: ScoringState) -> ScoringState:
        limit = asyncio.Semaphore(self._deps.summary_concurrency)
        scored = await asyncio.gather(*(self._explain(item, limit) for item in state["scored"]))
        return {"scored": list(scored)}

    async def publish(self, state: ScoringState) -> ScoringState:
        await self._deps.store.publish(state["run_id"], state["scored"])
        await self._deps.events.run_published(state["run_id"], state["status_changes"])
        return {"published": True}
