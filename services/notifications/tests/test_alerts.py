from collections.abc import AsyncIterator
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from voc_data.enums import RunStatus, Urgency
from voc_data.models import Account, Base, Notification, RefreshRun, StatusChangeEvent

from notifier.alerts import send_status_alerts

BASE_URL = "https://voc.example.navex.com"


class FakeMailer:
    def __init__(self, fail_for: str | None = None) -> None:
        self.sent: list[tuple[str, str, str, str]] = []
        self._fail_for = fail_for

    def send(self, to: str, subject: str, text: str, html: str) -> None:
        if to == self._fail_for:
            raise ConnectionError
        self.sent.append((to, subject, text, html))


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as db:
        yield db
    await engine.dispose()


async def _seed(db: AsyncSession) -> UUID:
    run = RefreshRun(run_id=uuid4(), status=RunStatus.SUCCESS)
    db.add(run)
    changes = [
        ("001A", "Crestview <Pharma>", "cxm1@navex.com", "G", "R", Urgency.ACTION_NEEDED),
        ("001B", "Alder and Pine", "cxm1@navex.com", "R", "Y", Urgency.FYI),
        ("001C", "Thames Retail", "cxm2@navex.com", "R", "Y", Urgency.FYI),
    ]
    for sfdc_id, name, owner, before, after, urgency in changes:
        account = Account(
            account_id=uuid4(), sfdc_account_id=sfdc_id, name=name, segment="Enterprise",
            region="AMER", arr=Decimal("290000"), next_renewal_date=date(2027, 1, 31),
            cxm_owner_upn=owner, products=[],
        )  # fmt: skip
        db.add(account)
        await db.flush()
        db.add(
            StatusChangeEvent(
                account_id=account.account_id, run_id=run.run_id,
                from_status=before, to_status=after, urgency=urgency,
            )
        )  # fmt: skip
    await db.commit()
    return run.run_id


async def test_one_batched_email_per_owner_marked_action_or_fyi(session: AsyncSession) -> None:
    run_id = await _seed(session)
    mailer = FakeMailer()

    assert await send_status_alerts(session, mailer, run_id, BASE_URL) == 2

    subjects = {to: subject for to, subject, _, _ in mailer.sent}
    assert subjects["cxm1@navex.com"] == "Action needed: 2 accounts changed VoC status"
    assert subjects["cxm2@navex.com"] == "FYI: 1 account changed VoC status"
    text = next(text for to, _, text, _ in mailer.sent if to == "cxm1@navex.com")
    assert f"{BASE_URL}/accounts/001A?src=alert&event=" in text


async def test_html_email_escapes_account_names(session: AsyncSession) -> None:
    run_id = await _seed(session)
    mailer = FakeMailer()
    await send_status_alerts(session, mailer, run_id, BASE_URL)
    html = next(html for to, _, _, html in mailer.sent if to == "cxm1@navex.com")
    assert "Crestview &lt;Pharma&gt;" in html


async def test_rerun_sends_nothing_twice(session: AsyncSession) -> None:
    run_id = await _seed(session)
    mailer = FakeMailer()
    await send_status_alerts(session, mailer, run_id, BASE_URL)
    assert await send_status_alerts(session, mailer, run_id, BASE_URL) == 0
    assert len(mailer.sent) == 2


async def test_failed_recipient_is_retried_without_resending_to_others(
    session: AsyncSession,
) -> None:
    run_id = await _seed(session)
    assert await send_status_alerts(session, FakeMailer("cxm2@navex.com"), run_id, BASE_URL) == 1

    retry = FakeMailer()
    assert await send_status_alerts(session, retry, run_id, BASE_URL) == 1
    assert [to for to, *_ in retry.sent] == ["cxm2@navex.com"]
    assert await session.scalar(select(func.count()).select_from(Notification)) == 3
