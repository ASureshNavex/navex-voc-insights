"""PostgreSQL serving store. A run becomes visible only when `published_run` switches."""

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from voc_data.enums import Rating, RunStatus
from voc_data.models import (
    Account,
    AccountFeedbackBatch,
    AccountRating,
    AccountStatusState,
    AccountTheme,
    PublishedRun,
    RefreshRun,
    StatusChangeEvent,
    Theme,
    VerbatimRef,
    WeeklySnapshot,
)

from account_scoring_agent.domain.models import (
    AccountInput,
    DriverVerbatim,
    ScoredAccount,
    StatusState,
    ThemeCount,
)


def _week_start(today: date) -> date:
    return today - timedelta(days=today.weekday())


class SqlServingStore:
    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def load_batch(self, run_id: str) -> list[AccountInput]:
        this_week = _week_start(datetime.now(UTC).date())
        async with self._sessions() as session:
            theme_names = dict((await session.execute(select(Theme.theme_id, Theme.name))).all())
            states = {s.account_id: s for s in await session.scalars(select(AccountStatusState))}
            previous = dict(
                (
                    await session.execute(
                        select(WeeklySnapshot.account_id, WeeklySnapshot.status).where(
                            WeeklySnapshot.week_start == this_week - timedelta(days=7)
                        )
                    )
                ).all()
            )
            rows = await session.execute(
                select(AccountFeedbackBatch, Account)
                .join(Account, Account.account_id == AccountFeedbackBatch.account_id)
                .where(AccountFeedbackBatch.run_id == UUID(run_id))
                .order_by(Account.account_id)
            )
            return [
                self._to_input(batch, account, theme_names, states, previous)
                for batch, account in rows
            ]

    @staticmethod
    def _to_input(
        batch: AccountFeedbackBatch,
        account: Account,
        theme_names: dict[str, str],
        states: dict[UUID, AccountStatusState],
        previous: dict[UUID, str],
    ) -> AccountInput:
        state = states.get(account.account_id)
        last_week = previous.get(account.account_id)
        return AccountInput(
            account_id=str(account.account_id),
            name=account.name,
            products=tuple(account.products),
            feedback_count=batch.feedback_count,
            churn_language=batch.churn_language,
            voc_sentiment=batch.voc_sentiment,
            previous_week_status=Rating(last_week) if last_week else None,
            state=StatusState(
                Rating(state.confirmed_status),
                Rating(state.pending_status) if state.pending_status else None,
                state.pending_runs,
            )
            if state
            else None,
            theme_counts=tuple(
                ThemeCount(
                    theme_id=count["theme_id"],
                    name=theme_names.get(count["theme_id"], count["theme_id"]),
                    volume=count["volume"],
                    negative_volume=count["negative_volume"],
                )
                for count in batch.theme_counts
            ),
            verbatims=tuple(
                DriverVerbatim(
                    verbatim_id=v["verbatim_id"],
                    theme_id=v.get("theme_id"),
                    source=v["source"],
                    feedback_date=date.fromisoformat(v["feedback_date"]),
                    product=v.get("product"),
                    text=v["text"],
                    citation_url=v.get("citation_url"),
                )
                for v in batch.verbatims
            ),
        )

    async def cached_explanation(self, account_id: str, evidence_hash: str) -> str | None:
        async with self._sessions() as session:
            return await session.scalar(
                select(AccountRating.explanation)
                .join(PublishedRun, PublishedRun.run_id == AccountRating.run_id)
                .where(
                    AccountRating.account_id == UUID(account_id),
                    AccountRating.explanation_hash == evidence_hash,
                )
            )

    async def publish(self, run_id: str, scored: list[ScoredAccount]) -> None:
        run_uuid = UUID(run_id)
        now = datetime.now(UTC)
        this_week = _week_start(now.date())
        async with self._sessions() as session, session.begin():
            arr = dict((await session.execute(select(Account.account_id, Account.arr))).all())
            for item in scored:
                account_id = UUID(item.account.account_id)
                previous = item.account.previous_week_status
                session.add(
                    AccountRating(
                        account_id=account_id,
                        run_id=run_uuid,
                        status=item.decision.rating,
                        previous_status=previous,
                        score=Decimal(str(item.decision.score)),
                        rule_code=item.trigger.code,
                        rule_text=item.trigger.text,
                        confidence=item.decision.confidence,
                        churn_language=item.account.churn_language,
                        voc_sentiment=item.account.voc_sentiment,
                        explanation=item.explanation,
                        explanation_hash=item.explanation_hash,
                        feedback_count=item.account.feedback_count,
                        rule_set_version=item.decision.rule_set_version,
                    )
                )
                session.add_all(
                    AccountTheme(
                        account_id=account_id,
                        theme_id=theme.theme_id,
                        run_id=run_uuid,
                        volume=theme.volume,
                        negative_volume=theme.negative_volume,
                        rank=theme.rank,
                        is_primary=theme.is_primary,
                    )
                    for theme in item.themes
                )
                session.add_all(
                    VerbatimRef(
                        verbatim_id=v.verbatim_id,
                        run_id=run_uuid,
                        account_id=account_id,
                        theme_id=v.theme_id,
                        source=v.source,
                        feedback_date=v.feedback_date,
                        product=v.product,
                        masked_excerpt=v.text,
                        citation_url=v.citation_url,
                    )
                    for v in item.drivers
                )
                await session.merge(
                    AccountStatusState(
                        account_id=account_id,
                        confirmed_status=item.state.confirmed_status,
                        pending_status=item.state.pending_status,
                        pending_runs=item.state.pending_runs,
                    )
                )
                await session.merge(
                    WeeklySnapshot(
                        week_start=this_week,
                        account_id=account_id,
                        status=item.decision.rating,
                        score=Decimal(str(item.decision.score)),
                        arr=arr[account_id],
                    )
                )
                if item.change:
                    session.add(
                        StatusChangeEvent(
                            account_id=account_id,
                            run_id=run_uuid,
                            from_status=item.change.from_status,
                            to_status=item.change.to_status,
                            urgency=item.change.urgency,
                        )
                    )
            run = await session.get_one(RefreshRun, run_uuid)
            run.status = RunStatus.SUCCESS
            run.finished_at = now
            run.rule_set_version = scored[0].decision.rule_set_version if scored else None
            await session.merge(PublishedRun(id=1, run_id=run_uuid, published_at=now))

    async def fail_run(self, run_id: str, note: str) -> None:
        async with self._sessions() as session, session.begin():
            run = await session.get_one(RefreshRun, UUID(run_id))
            run.status = RunStatus.FAILED
            run.finished_at = datetime.now(UTC)
            run.note = note
