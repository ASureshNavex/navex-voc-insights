from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

Schedule = Literal["daily", "weekdays", "weekly_monday", "monthly_first"]


class DigestContent(BaseModel):
    red_accounts: bool = True
    yellow_accounts: bool = True
    new_red_this_week: bool = True
    overdue_red_responses: bool = True
    renewals_next_90_days: bool = True


class DigestResponse(BaseModel):
    digest_id: UUID
    name: str
    audience: str
    schedule: Schedule
    send_time: str
    next_run_at: datetime | None
    archive_days: int
    is_active: bool
    content: DigestContent


class DigestUpdate(BaseModel):
    schedule: Schedule | None = None
    send_time: str | None = None
    is_active: bool | None = None
    content: DigestContent | None = None


class DigestPreview(BaseModel):
    subject: str
    body_text: str


class ArchivedDigest(BaseModel):
    name: str
    sent_at: datetime
    archived_on: datetime
    accounts_needing_attention: int


class DigestPreference(BaseModel):
    digest_id: UUID
    name: str
    enabled: bool
