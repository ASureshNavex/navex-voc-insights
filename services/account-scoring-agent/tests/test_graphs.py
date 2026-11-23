from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from voc_data.enums import RunStatus
from voc_data.models import (
    Account,
    AccountFeedbackBatch,
    AccountRating,
    Base,
    PublishedRun,
    RefreshRun,
    Theme,
    VerbatimRef,
)

from account_scoring_agent.domain.scoring import ThresholdRuleSet
from account_scoring_agent.graphs.account_scoring.graph import run_scoring
from account_scoring_agent.graphs.account_scoring.nodes import Dependencies
from account_scoring_agent.schemas.outputs import AccountSummary
from account_scoring_agent.schemas.prompt_contexts import AccountSummaryContext
from account_scoring_agent.tools.serving_store import SqlServingStore

EXPLANATION = "Customers report that completion counts in reports are lower than expected."


class FakeSummariser:
    def __init__(self, cite: str = "v1", fail: bool = False) -> None:
        self.calls = 0
        self._cite, self._fail = cite, fail

    async def summarise(self, context: AccountSummaryContext) -> AccountSummary:
        self.calls += 1
        if self._fail:
            raise TimeoutError
        return AccountSummary(explanation=EXPLANATION, cited_verbatim_ids=[self._cite])


class FakeEvents:
    def __init__(self) -> None:
        self.published: list[tuple[str, int]] = []

    async def run_published(self, run_id: str, status_changes: int) -> None:
        self.published.append((run_id, status_changes))


@pytest.fixture
async def sessions():  # type: ignore[no-untyped-def]
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


async def _stage_run(sessions, with_batch: bool = True) -> str:  # type: ignore[no-untyped-def]
    async with sessions() as session:
        run = RefreshRun(run_id=uuid4(), status=RunStatus.RUNNING)
        account = await session.scalar(select(Account))
        if account is None:
            account = Account(
                account_id=uuid4(), sfdc_account_id="001A", name="Crestview Pharma",
                segment="Enterprise", region="AMER", arr=Decimal("290000"),
                products=["Compliance Training"],
            )  # fmt: skip
            session.add_all(
                [account, Theme(theme_id="t1", level1="Reporting", name="Report accuracy")]
            )
        session.add(run)
        await session.flush()
        if with_batch:
            session.add(
                AccountFeedbackBatch(
                    run_id=run.run_id, account_id=account.account_id, feedback_count=10,
                    churn_language=False, voc_sentiment="Negative",
                    theme_counts=[{"theme_id": "t1", "volume": 10, "negative_volume": 8}],
                    verbatims=[{"verbatim_id": "v1", "theme_id": "t1", "source": "Support case",
                                "feedback_date": date(2026, 11, 3).isoformat(), "product": None,
                                "text": "Completion counts in the report are lower."}],
                )
            )  # fmt: skip
        await session.commit()
        return str(run.run_id)


def _deps(sessions, summariser: FakeSummariser, events: FakeEvents) -> Dependencies:  # type: ignore[no-untyped-def]
    return Dependencies(
        store=SqlServingStore(sessions),
        rules=ThresholdRuleSet(version="test", red_above=65, yellow_from=35),
        summariser=summariser,
        events=events,
    )


async def test_run_scores_explains_and_publishes(sessions) -> None:  # type: ignore[no-untyped-def]
    events = FakeEvents()
    run_id = await _stage_run(sessions)

    state = await run_scoring(_deps(sessions, FakeSummariser(), events), run_id)

    assert state["published"] is True
    assert events.published == [(run_id, 0)]
    async with sessions() as session:
        rating = (await session.scalars(select(AccountRating))).one()
        assert (rating.status, rating.rule_code, rating.explanation) == ("R", "AR1", EXPLANATION)
        assert str((await session.scalars(select(PublishedRun))).one().run_id) == run_id
        assert (await session.scalars(select(VerbatimRef))).one().verbatim_id == "v1"


async def test_unchanged_evidence_reuses_the_explanation(sessions) -> None:  # type: ignore[no-untyped-def]
    first, second = FakeSummariser(), FakeSummariser()
    await run_scoring(_deps(sessions, first, FakeEvents()), await _stage_run(sessions))
    await run_scoring(_deps(sessions, second, FakeEvents()), await _stage_run(sessions))
    assert (first.calls, second.calls) == (1, 0)


@pytest.mark.parametrize("summariser", [FakeSummariser(fail=True), FakeSummariser(cite="v9")])
async def test_failed_or_ungrounded_summary_still_publishes_the_rating(  # type: ignore[no-untyped-def]
    sessions, summariser: FakeSummariser
) -> None:
    state = await run_scoring(_deps(sessions, summariser, FakeEvents()), await _stage_run(sessions))
    assert state["published"] is True
    async with sessions() as session:
        assert (await session.scalars(select(AccountRating))).one().explanation is None


async def test_empty_batch_fails_the_run_and_publishes_nothing(sessions) -> None:  # type: ignore[no-untyped-def]
    events = FakeEvents()
    run_id = await _stage_run(sessions, with_batch=False)

    state = await run_scoring(_deps(sessions, FakeSummariser(), events), run_id)

    assert state["published"] is False and events.published == []
    async with sessions() as session:
        assert (await session.scalars(select(RefreshRun))).one().status == RunStatus.FAILED
        assert (await session.scalars(select(PublishedRun))).first() is None
