from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field
from voc_data.enums import Rating

StatusTag = Literal["new_red", "repeat_red", "new_yellow"]


class AccountFilters(BaseModel):
    """Scorecard list query. Filters only ever narrow within the caller's scope."""

    status: list[Rating] = Field(default_factory=lambda: list(Rating))
    q: str | None = Field(default=None, max_length=120)
    segment: str | None = None
    arr_tier: Literal["50k_plus", "under_50k"] | None = None
    region: str | None = None
    exec_sponsor: str | None = None
    account_executive: str | None = None
    super_product_family: str | None = None
    theme: str | None = None
    issue_status: str | None = None
    renewal_window: Literal["within_180", "beyond_180"] | None = None
    new_only: bool = False
    cxm: str | None = None
    team: str | None = None
    sort: Literal["priority", "arr", "renewal"] = "priority"


class Rule(BaseModel):
    code: str
    text: str


class Nps(BaseModel):
    category: str
    date: date | None


class ThemeChip(BaseModel):
    theme_id: str
    name: str
    path: str
    negative_volume: int
    is_primary: bool


class Verbatim(BaseModel):
    verbatim_id: str
    text: str
    source: str
    feedback_date: date
    product: str | None
    citation_url: str | None


class AccountRow(BaseModel):
    sfdc_account_id: str
    name: str
    rating: Rating
    previous_rating: Rating | None
    status_tag: StatusTag | None
    churn_language: bool
    arr: Decimal
    region: str
    segment: str
    team: str | None
    cxm: str | None
    exec_sponsor: str | None
    account_executive: str | None
    next_renewal_date: date | None
    rule: Rule
    issue_status: str | None
    nps: Nps | None
    products: list[str]
    super_product_family: str | None
    explanation: str | None
    themes: list[ThemeChip]
    top_verbatim: Verbatim | None


class TrendPoint(BaseModel):
    week_start: date
    score: Decimal | None
    rating: Rating


class AccountDetail(AccountRow):
    churn_score: Decimal | None
    churn_score_as_of: date | None
    voc_sentiment: str | None
    feedback_count: int
    verbatims: list[Verbatim]
    friction_trend: list[TrendPoint]


class AccountBrief(BaseModel):
    sfdc_account_id: str
    prepared_on: date
    text: str
