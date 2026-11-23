from collections.abc import AsyncIterator
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from voc_data.enums import DataScope, Ownership
from voc_data.models import Account, Base, Person
from voc_data.scope import AccessScope, scope_filter


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as db:
        db.add_all(
            [
                Person(upn="lead@navex.com", display_name="Lead", manager_upn=None),
                Person(upn="cxm1@navex.com", display_name="One", manager_upn="lead@navex.com"),
                Person(upn="cxm2@navex.com", display_name="Two", manager_upn="lead@navex.com"),
                Person(upn="other@navex.com", display_name="Other", manager_upn=None),
                _account("001A", "cxm1@navex.com", "ae1@navex.com", "AMER"),
                _account("001B", "cxm2@navex.com", "ae1@navex.com", "EMEA/APJ"),
                _account("001C", "other@navex.com", "ae2@navex.com", "AMER"),
            ]
        )
        await db.commit()
        yield db
    await engine.dispose()


def _account(sfdc_id: str, cxm: str, ae: str, region: str) -> Account:
    return Account(
        sfdc_account_id=sfdc_id,
        name=sfdc_id,
        segment="Enterprise",
        region=region,
        arr=Decimal("100000"),
        cxm_owner_upn=cxm,
        ae_owner_upn=ae,
        products=[],
    )


async def _visible(session: AsyncSession, scope: AccessScope) -> set[str]:
    rows = await session.scalars(select(Account.sfdc_account_id).where(scope_filter(scope)))
    return set(rows)


async def test_own_book_returns_only_owned_accounts(session: AsyncSession) -> None:
    scope = AccessScope("cxm1@navex.com", DataScope.OWN_BOOK, Ownership.CXM)
    assert await _visible(session, scope) == {"001A"}


async def test_team_includes_reports_and_excludes_other_teams(session: AsyncSession) -> None:
    scope = AccessScope("lead@navex.com", DataScope.TEAM, Ownership.CXM)
    assert await _visible(session, scope) == {"001A", "001B"}


async def test_account_executive_scope_follows_ae_ownership(session: AsyncSession) -> None:
    scope = AccessScope("ae1@navex.com", DataScope.OWN_BOOK, Ownership.ACCOUNT_EXECUTIVE)
    assert await _visible(session, scope) == {"001A", "001B"}


async def test_region_without_a_region_sees_nothing(session: AsyncSession) -> None:
    scope = AccessScope("x@navex.com", DataScope.REGION, Ownership.CXM)
    assert await _visible(session, scope) == set()


async def test_all_sees_everything(session: AsyncSession) -> None:
    scope = AccessScope("admin@navex.com", DataScope.ALL, Ownership.CXM)
    assert await _visible(session, scope) == {"001A", "001B", "001C"}
