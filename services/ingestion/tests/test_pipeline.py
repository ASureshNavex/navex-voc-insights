from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from voc_data.enums import RunStatus
from voc_data.models import Account, AccountFeedbackBatch, Base, RefreshRun

from ingestion.adapters.staging import SqlStagingStore
from ingestion.masking import mask_personal_details
from ingestion.models import (
    AccountFeedback,
    SourceAccount,
    SourceVerbatim,
    TaxonomyTheme,
    ThemeCount,
)
from ingestion.pipeline import Dependencies, run_ingestion

ACCOUNT = SourceAccount(
    sfdc_account_id="001A", name="Crestview Pharma", segment="Enterprise", region="AMER",
    arr=Decimal("290000"), cxm_owner_upn="cxm1@navex.com",
)  # fmt: skip
THEME = TaxonomyTheme(theme_id="t1", level1="Reporting", name="Report accuracy")


def _feedback(sfdc_account_id: str) -> AccountFeedback:
    return AccountFeedback(
        sfdc_account_id=sfdc_account_id,
        feedback_count=3,
        theme_counts=[ThemeCount(theme_id="t1", volume=3, negative_volume=2)],
        verbatims=[
            SourceVerbatim(
                verbatim_id=f"v-{sfdc_account_id}",
                source="Support case",
                feedback_date=date(2026, 11, 3),
                text="Call me on +1 (503) 555-0100 or write to dana@example.com about the export.",
            )
        ],
    )


class FakeAccounts:
    async def fetch_accounts(self) -> list[SourceAccount]:
        return [ACCOUNT]


class FakeFeedback:
    def __init__(self, fail: bool = False) -> None:
        self._fail = fail

    async def fetch_taxonomy(self) -> list[TaxonomyTheme]:
        return [THEME]

    async def fetch_feedback(self, window_days: int) -> list[AccountFeedback]:
        if self._fail:
            raise TimeoutError
        return [_feedback("001A"), _feedback("001-UNKNOWN")]


class FakeAgent:
    def __init__(self) -> None:
        self.started: list[str] = []

    async def start(self, run_id: str) -> None:
        self.started.append(run_id)


@pytest.fixture
async def sessions():  # type: ignore[no-untyped-def]
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


def test_masking_removes_email_and_phone() -> None:
    masked = mask_personal_details("Reach dana@example.com or +1 (503) 555-0100 today.")
    assert masked == "Reach [email] or [phone] today."


async def test_run_stages_matched_feedback_masked_and_starts_the_agent(sessions) -> None:  # type: ignore[no-untyped-def]
    agent = FakeAgent()
    deps = Dependencies(FakeAccounts(), FakeFeedback(), SqlStagingStore(sessions), agent, 90)

    result = await run_ingestion(deps)

    assert result is not None
    assert (result.accounts, result.matched, result.unmatched_records) == (1, 1, 3)
    assert agent.started == [result.run_id]
    async with sessions() as session:
        batch = (await session.scalars(select(AccountFeedbackBatch))).one()
        assert "[email]" in batch.verbatims[0]["text"]
        assert "555" not in batch.verbatims[0]["text"]
        assert (await session.scalars(select(Account))).one().name == "Crestview Pharma"


async def test_source_failure_fails_the_run_and_does_not_start_the_agent(sessions) -> None:  # type: ignore[no-untyped-def]
    agent = FakeAgent()
    deps = Dependencies(
        FakeAccounts(), FakeFeedback(fail=True), SqlStagingStore(sessions), agent, 90
    )

    with pytest.raises(TimeoutError):
        await run_ingestion(deps)

    assert agent.started == []
    async with sessions() as session:
        assert (await session.scalars(select(RefreshRun))).one().status == RunStatus.FAILED


async def test_second_run_is_skipped_while_one_is_active(sessions) -> None:  # type: ignore[no-untyped-def]
    store = SqlStagingStore(sessions)
    assert await store.start_run() is not None
    deps = Dependencies(FakeAccounts(), FakeFeedback(), store, FakeAgent(), 90)
    assert await run_ingestion(deps) is None
