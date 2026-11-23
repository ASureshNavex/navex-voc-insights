from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from voc_data.enums import Rating
from voc_data.models import Account, AccountRating, PublishedRun
from voc_data.scope import scope_filter

from app.core.entitlements import CurrentUser
from app.domains.portfolio.schemas import AccountRef, PortfolioSummary, RatingCard, SegmentCard

SEGMENT_CARDS = ("Enterprise", "MidMarket", "SMB")

type Rated = tuple[Account, AccountRating]


def _refs(rows: list[Rated]) -> list[AccountRef]:
    ordered = sorted(rows, key=lambda row: row[0].arr, reverse=True)
    return [
        AccountRef(sfdc_account_id=a.sfdc_account_id, name=a.name, arr=a.arr) for a, _ in ordered
    ]


def _arr(rows: list[Rated]) -> Decimal:
    return sum((account.arr for account, _ in rows), Decimal(0))


def _card(rows: list[Rated], rating: Rating, new_from: set[str | None]) -> RatingCard:
    rated = [row for row in rows if row[1].status == rating]
    return RatingCard(
        count=len(rated),
        arr=_arr(rated),
        new_this_week=_refs([row for row in rated if row[1].previous_status in new_from]),
        repeat=_refs([row for row in rated if row[1].previous_status == rating]),
    )


def _segment(rows: list[Rated], segment: str | None) -> SegmentCard:
    scoped = [row for row in rows if segment is None or row[0].segment == segment]
    red = [row for row in scoped if row[1].status == Rating.RED]
    yellow = [row for row in scoped if row[1].status == Rating.YELLOW]
    return SegmentCard(
        segment=segment,
        red_count=len(red),
        red_arr=_arr(red),
        yellow_count=len(yellow),
        yellow_arr=_arr(yellow),
    )


async def get_summary(session: AsyncSession, user: CurrentUser) -> PortfolioSummary:
    published = await session.scalar(select(PublishedRun))
    result = await session.execute(
        select(Account, AccountRating)
        .join(AccountRating, AccountRating.account_id == Account.account_id)
        .join(PublishedRun, PublishedRun.run_id == AccountRating.run_id)
        .where(scope_filter(user.access_scope))
    )
    rows = [(account, rating) for account, rating in result]
    return PortfolioSummary(
        total_accounts=len(rows),
        # New red: not red last week. New yellow: green last week.
        red=_card(rows, Rating.RED, {Rating.YELLOW, Rating.GREEN, None}),
        yellow=_card(rows, Rating.YELLOW, {Rating.GREEN}),
        segments=[_segment(rows, None), *(_segment(rows, name) for name in SEGMENT_CARDS)],
        last_refresh_at=published.published_at if published else None,
        next_refresh_at=published.next_refresh_at if published else None,
    )
