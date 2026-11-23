from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from voc_data.models import AuditEvent

from app.core.entitlements import CurrentUser


def record_audit(session: AsyncSession, user: CurrentUser, action: str, **detail: Any) -> None:
    """Queue an audit row on the caller's transaction, so both commit together."""
    session.add(AuditEvent(actor_upn=user.upn, action=action, detail=detail))
