from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from voc_data.enums import RunStatus
from voc_data.models import Account, AccountFeedbackBatch, RefreshRun, Theme

from ingestion.models import AccountFeedback, SourceAccount, TaxonomyTheme


class SqlStagingStore:
    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def start_run(self) -> str | None:
        async with self._sessions() as session:
            active = await session.scalar(
                select(RefreshRun.run_id).where(RefreshRun.status == RunStatus.RUNNING).limit(1)
            )
            if active is not None:
                return None
            run = RefreshRun(status=RunStatus.RUNNING)
            session.add(run)
            await session.commit()
            return str(run.run_id)

    async def stage(
        self,
        run_id: str,
        accounts: list[SourceAccount],
        themes: list[TaxonomyTheme],
        feedback: list[AccountFeedback],
        unmatched_records: int,
    ) -> None:
        async with self._sessions() as session:
            existing = {
                account.sfdc_account_id: account
                for account in await session.scalars(select(Account))
            }
            for source in accounts:
                values = source.model_dump()
                account = existing.get(source.sfdc_account_id)
                if account is None:
                    account = Account(**values)
                    session.add(account)
                    existing[source.sfdc_account_id] = account
                else:
                    for field, value in values.items():
                        setattr(account, field, value)
            for theme in themes:
                await session.merge(Theme(**theme.model_dump()))
            await session.flush()

            for item in feedback:
                session.add(
                    AccountFeedbackBatch(
                        run_id=UUID(run_id),
                        account_id=existing[item.sfdc_account_id].account_id,
                        feedback_count=item.feedback_count,
                        churn_language=item.churn_language,
                        voc_sentiment=item.voc_sentiment,
                        theme_counts=[count.model_dump() for count in item.theme_counts],
                        verbatims=[v.model_dump(mode="json") for v in item.verbatims],
                    )
                )
            run = await session.get_one(RefreshRun, UUID(run_id))
            run.accounts_processed = len(accounts)
            run.unmatched_records = unmatched_records
            await session.commit()

    async def fail_run(self, run_id: str, note: str) -> None:
        async with self._sessions() as session:
            run = await session.get_one(RefreshRun, UUID(run_id))
            run.status = RunStatus.FAILED
            run.finished_at = datetime.now(UTC)
            run.note = note
            await session.commit()
