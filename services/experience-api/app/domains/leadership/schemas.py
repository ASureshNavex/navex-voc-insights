from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from voc_data.enums import Rating


class CxmPerformance(BaseModel):
    cxm: str
    red_accounts: int
    responded_in_window: int | None
    overdue: int | None
    average_days_to_respond: Decimal | None
    hours_spent: Decimal | None
    high_arr_accounts: int
    high_arr_at_red: int
    impacted_arr: Decimal


class ManagerSummary(BaseModel):
    brief: str
    most_red_cxm: str | None
    most_arr_at_risk_cxm: str | None
    overdue_responses: int | None
    response_window_days: int
    team: list[CxmPerformance]


class ReportTemplate(BaseModel):
    template_id: UUID
    name: str
    filter_summary: str
    matching_accounts: int


class FrictionReportRow(BaseModel):
    sfdc_account_id: str
    name: str
    cxm: str | None
    segment: str
    products: list[str]
    theme: str | None
    rating: Rating
    previous_rating: Rating | None
    arr: Decimal
    next_renewal_date: date | None
