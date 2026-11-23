from collections.abc import AsyncIterator
from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from voc_data.enums import DataScope, Role, RunStatus
from voc_data.models import (
    Account,
    AccountRating,
    AccountTheme,
    Base,
    Person,
    PublishedRun,
    RefreshRun,
    Theme,
    VerbatimRef,
)

from app.core.database import get_session
from app.core.entitlements import PERMISSIONS, CurrentUser, get_current_user
from app.main import create_app

LEAD = "lead@navex.com"
CXM_ONE = "cxm1@navex.com"
CXM_TWO = "cxm2@navex.com"


def make_user(upn: str, role: Role, scope: DataScope) -> CurrentUser:
    return CurrentUser(
        upn=upn, name=upn, role=role, data_scope=scope, permissions=PERMISSIONS[role]
    )


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        "sqlite+aiosqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as db:
        await _seed(db)
        yield db
    await engine.dispose()


async def _seed(db: AsyncSession) -> None:
    run = RefreshRun(run_id=uuid4(), status=RunStatus.SUCCESS, rule_set_version="test")
    theme = Theme(theme_id="t1", level1="Reporting", level2="Accuracy", name="Report accuracy")
    db.add_all(
        [
            run,
            theme,
            Person(upn=LEAD, display_name="Lead"),
            Person(upn=CXM_ONE, display_name="One", manager_upn=LEAD),
            Person(upn=CXM_TWO, display_name="Two", manager_upn=LEAD),
        ]
    )
    await db.flush()
    db.add(PublishedRun(run_id=run.run_id))
    specs = [
        ("001A", "Crestview Pharma", CXM_ONE, "R", "G", Decimal("290000"), True),
        ("001B", "Alder and Pine Retail", CXM_ONE, "Y", "Y", Decimal("96000"), False),
        ("001C", "Northwind Financial", CXM_TWO, "R", "R", Decimal("420000"), False),
        ("001D", "Harbor Logistics", CXM_TWO, "G", "G", Decimal("40000"), False),
    ]
    for sfdc_id, name, owner, status, previous, arr, churn in specs:
        account = Account(
            account_id=uuid4(),
            sfdc_account_id=sfdc_id,
            name=name,
            segment="Enterprise",
            region="AMER",
            arr=arr,
            next_renewal_date=date(2027, 1, 31),
            cxm_owner_upn=owner,
            ae_owner_upn="ae@navex.com",
            products=["Compliance Training"],
        )
        db.add(account)
        await db.flush()
        db.add(
            AccountRating(
                account_id=account.account_id,
                run_id=run.run_id,
                status=status,
                previous_status=previous,
                rule_code="AR1" if status == "R" else "AG0",
                rule_text="New red this week" if status == "R" else "No rule matched",
                churn_language=churn,
                rule_set_version="test",
            )
        )
        if status == "R":
            db.add(
                AccountTheme(
                    account_id=account.account_id,
                    theme_id="t1",
                    run_id=run.run_id,
                    volume=5,
                    negative_volume=4,
                    rank=1,
                    is_primary=True,
                )
            )
            db.add(
                VerbatimRef(
                    verbatim_id=f"v-{sfdc_id}",
                    run_id=run.run_id,
                    account_id=account.account_id,
                    theme_id="t1",
                    source="Support case",
                    feedback_date=date(2026, 11, 3),
                    masked_excerpt="Completion counts in the report are lower than expected.",
                )
            )
    await db.commit()


@pytest.fixture
async def client_for(session: AsyncSession):  # type: ignore[no-untyped-def]
    """Build an API client that is signed in as the given user."""
    clients: list[AsyncClient] = []

    async def build(user: CurrentUser) -> AsyncClient:
        app = create_app()
        app.dependency_overrides[get_session] = lambda: session
        app.dependency_overrides[get_current_user] = lambda: user
        client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1")
        clients.append(client)
        return client

    yield build
    for client in clients:
        await client.aclose()
