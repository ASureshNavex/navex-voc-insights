from collections import defaultdict
from collections.abc import Sequence
from datetime import date, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import ColumnElement, Select, and_, case, exists, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from voc_data.enums import Rating
from voc_data.models import (
    Account,
    AccountRating,
    AccountTheme,
    PublishedRun,
    Theme,
    VerbatimRef,
    WeeklySnapshot,
)
from voc_data.scope import scope_filter

from app.core.entitlements import CurrentUser
from app.core.exceptions import NotFound
from app.core.pagination import Page, PageParams
from app.domains.accounts.schemas import (
    AccountDetail,
    AccountFilters,
    AccountRow,
    Nps,
    Rule,
    StatusTag,
    ThemeChip,
    TrendPoint,
    Verbatim,
)

TREND_WEEKS = 12
ARR_TIER_BOUNDARY = 50_000
RENEWAL_WINDOW_DAYS = 180

_IS_NEW = or_(
    and_(AccountRating.status == Rating.RED, AccountRating.previous_status != Rating.RED),
    and_(AccountRating.status == Rating.YELLOW, AccountRating.previous_status == Rating.GREEN),
)

# Red accounts with churn language first, then other red, then yellow, then green.
_PRIORITY = case(
    (and_(AccountRating.status == Rating.RED, AccountRating.churn_language), 0),
    (AccountRating.status == Rating.RED, 1),
    (AccountRating.status == Rating.YELLOW, 2),
    else_=3,
)

_SORTS: dict[str, tuple[ColumnElement[Any], ...]] = {
    "priority": (_PRIORITY, Account.arr.desc()),
    "arr": (Account.arr.desc(),),
    "renewal": (Account.next_renewal_date.asc(),),
}


def _published_accounts(user: CurrentUser) -> Select[Account, AccountRating]:
    """Accounts in the caller's scope with their rating from the published run only."""
    return (
        select(Account, AccountRating)
        .join(AccountRating, AccountRating.account_id == Account.account_id)
        .join(PublishedRun, PublishedRun.run_id == AccountRating.run_id)
        .where(scope_filter(user.access_scope))
    )


def _conditions(filters: AccountFilters) -> list[ColumnElement[bool]]:
    conditions: list[ColumnElement[bool]] = [AccountRating.status.in_(filters.status)]
    equals = {
        Account.segment: filters.segment,
        Account.region: filters.region,
        Account.exec_sponsor: filters.exec_sponsor,
        Account.ae_owner_upn: filters.account_executive,
        Account.super_product_family: filters.super_product_family,
        Account.issue_status: filters.issue_status,
        Account.cxm_owner_upn: filters.cxm,
        Account.team: filters.team,
    }
    conditions += [column == value for column, value in equals.items() if value]

    if filters.q:
        pattern = f"%{filters.q.strip()}%"
        conditions.append(
            or_(
                Account.name.ilike(pattern),
                Account.cxm_owner_upn.ilike(pattern),
                Account.ae_owner_upn.ilike(pattern),
                AccountRating.explanation.ilike(pattern),
            )
        )
    if filters.arr_tier:
        above = Account.arr >= ARR_TIER_BOUNDARY
        conditions.append(above if filters.arr_tier == "50k_plus" else ~above)
    if filters.renewal_window:
        within = Account.next_renewal_date <= date.today() + timedelta(days=RENEWAL_WINDOW_DAYS)
        conditions.append(within if filters.renewal_window == "within_180" else ~within)
    if filters.new_only:
        conditions.append(_IS_NEW)
    if filters.theme:
        conditions.append(
            exists().where(
                AccountTheme.account_id == Account.account_id,
                AccountTheme.run_id == AccountRating.run_id,
                AccountTheme.theme_id == Theme.theme_id,
                Theme.name == filters.theme,
            )
        )
    return conditions


def _status_tag(rating: AccountRating) -> StatusTag | None:
    if rating.status == Rating.RED:
        return "repeat_red" if rating.previous_status == Rating.RED else "new_red"
    if rating.status == Rating.YELLOW and rating.previous_status == Rating.GREEN:
        return "new_yellow"
    return None


def _to_verbatim(ref: VerbatimRef) -> Verbatim:
    return Verbatim(
        verbatim_id=ref.verbatim_id,
        text=ref.masked_excerpt,
        source=ref.source,
        feedback_date=ref.feedback_date,
        product=ref.product,
        citation_url=ref.citation_url,
    )


async def _themes(
    session: AsyncSession, run_id: UUID, account_ids: Sequence[UUID]
) -> dict[UUID, list[ThemeChip]]:
    rows = await session.execute(
        select(AccountTheme, Theme)
        .join(Theme, Theme.theme_id == AccountTheme.theme_id)
        .where(AccountTheme.run_id == run_id, AccountTheme.account_id.in_(account_ids))
        .order_by(AccountTheme.account_id, AccountTheme.rank, AccountTheme.theme_id)
    )
    themes: dict[UUID, list[ThemeChip]] = defaultdict(list)
    for link, theme in rows:
        path = " / ".join(part for part in (theme.level1, theme.level2, theme.level3) if part)
        themes[link.account_id].append(
            ThemeChip(
                theme_id=theme.theme_id,
                name=theme.name,
                path=path,
                negative_volume=link.negative_volume,
                is_primary=link.is_primary,
            )
        )
    return themes


async def _verbatims(
    session: AsyncSession, run_id: UUID, account_ids: Sequence[UUID]
) -> dict[UUID, list[Verbatim]]:
    rows = await session.scalars(
        select(VerbatimRef)
        .where(VerbatimRef.run_id == run_id, VerbatimRef.account_id.in_(account_ids))
        .order_by(VerbatimRef.account_id, VerbatimRef.feedback_date.desc(), VerbatimRef.verbatim_id)
    )
    verbatims: dict[UUID, list[Verbatim]] = defaultdict(list)
    for ref in rows:
        verbatims[ref.account_id].append(_to_verbatim(ref))
    return verbatims


def _to_row(
    account: Account, rating: AccountRating, themes: list[ThemeChip], verbatims: list[Verbatim]
) -> AccountRow:
    return AccountRow(
        sfdc_account_id=account.sfdc_account_id,
        name=account.name,
        rating=Rating(rating.status),
        previous_rating=Rating(rating.previous_status) if rating.previous_status else None,
        status_tag=_status_tag(rating),
        churn_language=rating.churn_language,
        arr=account.arr,
        region=account.region,
        segment=account.segment,
        team=account.team,
        cxm=account.cxm_owner_upn,
        exec_sponsor=account.exec_sponsor,
        account_executive=account.ae_owner_upn,
        next_renewal_date=account.next_renewal_date,
        rule=Rule(code=rating.rule_code, text=rating.rule_text),
        issue_status=account.issue_status,
        nps=Nps(category=account.nps_category, date=account.nps_date)
        if account.nps_category
        else None,
        products=account.products,
        super_product_family=account.super_product_family,
        explanation=rating.explanation,
        themes=themes,
        top_verbatim=verbatims[0] if verbatims else None,
    )


async def list_accounts(
    session: AsyncSession, user: CurrentUser, filters: AccountFilters, page: PageParams
) -> Page[AccountRow]:
    scoped = _published_accounts(user).where(*_conditions(filters))
    total = await session.scalar(select(func.count()).select_from(scoped.subquery())) or 0
    # The account ID is the tie-breaker, so pages never repeat or skip a row.
    rows = (
        await session.execute(
            scoped.order_by(*_SORTS[filters.sort], Account.account_id)
            .limit(page.limit)
            .offset(page.offset)
        )
    ).all()
    if not rows:
        return Page(items=[], total=total, limit=page.limit, offset=page.offset)

    run_id = rows[0][1].run_id
    account_ids = [account.account_id for account, _ in rows]
    themes = await _themes(session, run_id, account_ids)
    verbatims = await _verbatims(session, run_id, account_ids)
    items = [
        _to_row(account, rating, themes[account.account_id], verbatims[account.account_id])
        for account, rating in rows
    ]
    return Page(items=items, total=total, limit=page.limit, offset=page.offset)


async def get_account(
    session: AsyncSession, user: CurrentUser, sfdc_account_id: str
) -> AccountDetail:
    row = (
        await session.execute(
            _published_accounts(user).where(Account.sfdc_account_id == sfdc_account_id)
        )
    ).first()
    # Outside scope and unknown are deliberately the same answer.
    if row is None:
        raise NotFound("Account not found.")
    account, rating = row

    themes = await _themes(session, rating.run_id, [account.account_id])
    verbatims = await _verbatims(session, rating.run_id, [account.account_id])
    snapshots = await session.scalars(
        select(WeeklySnapshot)
        .where(WeeklySnapshot.account_id == account.account_id)
        .order_by(WeeklySnapshot.week_start.desc())
        .limit(TREND_WEEKS)
    )
    base = _to_row(account, rating, themes[account.account_id], verbatims[account.account_id])
    return AccountDetail(
        **base.model_dump(),
        churn_score=account.churn_score,
        churn_score_as_of=account.churn_score_as_of,
        voc_sentiment=rating.voc_sentiment,
        feedback_count=rating.feedback_count,
        verbatims=verbatims[account.account_id],
        friction_trend=[
            TrendPoint(week_start=s.week_start, score=s.score, rating=Rating(s.status))
            for s in reversed(snapshots.all())
        ],
    )
