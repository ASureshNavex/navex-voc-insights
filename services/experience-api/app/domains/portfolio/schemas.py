from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class AccountRef(BaseModel):
    sfdc_account_id: str
    name: str
    arr: Decimal


class RatingCard(BaseModel):
    count: int
    arr: Decimal
    new_this_week: list[AccountRef]
    repeat: list[AccountRef]


class SegmentCard(BaseModel):
    segment: str | None
    red_count: int
    red_arr: Decimal
    yellow_count: int
    yellow_arr: Decimal


class PortfolioSummary(BaseModel):
    total_accounts: int
    red: RatingCard
    yellow: RatingCard
    segments: list[SegmentCard]
    last_refresh_at: datetime | None
    next_refresh_at: datetime | None


class WeekShare(BaseModel):
    week_start: date
    total_count: int
    red_count: int
    yellow_count: int
    total_arr: Decimal
    red_arr: Decimal
    yellow_arr: Decimal


class PortfolioTrend(BaseModel):
    weeks: list[WeekShare]
