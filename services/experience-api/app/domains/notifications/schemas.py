from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NotificationItem(BaseModel):
    notification_id: UUID
    title: str
    created_at: datetime
    read: bool
    sfdc_account_id: str | None = None


class NotificationList(BaseModel):
    items: list[NotificationItem]
    unread: int
