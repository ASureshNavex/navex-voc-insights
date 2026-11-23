from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from voc_data.enums import DataScope, Rating, Role, RunStatus


class AuditEntry(BaseModel):
    occurred_at: datetime
    actor: str
    action: str


class AdminHome(BaseModel):
    excel_downloads_7_days: int
    last_refresh_at: datetime | None
    next_refresh_at: datetime | None
    published_files: int
    recent_activity: list[AuditEntry]


class WeeklyChange(BaseModel):
    sfdc_account_id: str
    name: str
    cxm: str | None
    from_rating: Rating
    to_rating: Rating
    theme: str | None
    arr: Decimal


class WeeklyChanges(BaseModel):
    new_red: list[WeeklyChange]
    repeat_red: list[WeeklyChange]


class LeadershipEmail(BaseModel):
    to: list[EmailStr] = Field(min_length=1, max_length=10)
    subject: str = Field(min_length=1, max_length=150)
    message: str = Field(min_length=1, max_length=20_000)


class SourceHealth(BaseModel):
    name: str
    status: Literal["Healthy", "Warning", "Failed", "Not connected"]
    last_sync_at: datetime | None
    records: int
    errors: int
    note: str | None


class RefreshRunRow(BaseModel):
    run_id: UUID
    started_at: datetime
    status: RunStatus | Literal["SCHEDULED"]
    accounts_processed: int | None
    note: str | None


class UsageHighlights(BaseModel):
    most_views_user: str | None
    top_cxm_by_views: str | None
    active_users_7_days: int
    total_users: int
    excel_downloads_7_days: int
    average_views_per_user: int


class UsageRow(BaseModel):
    key: str
    role: str | None = None
    team: str | None = None
    segment: str | None = None
    region: str | None = None
    users: int = 1
    last_login_at: datetime | None = None
    views_7_days: int
    active_weeks_of_4: int | None = None
    returned_this_week: int


class AccessRow(BaseModel):
    upn: str
    name: str
    role: Role
    data_scope: DataScope
    accounts_in_scope: int
