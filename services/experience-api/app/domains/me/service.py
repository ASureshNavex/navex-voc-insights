from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from voc_data.models import Account
from voc_data.scope import scope_filter

from app.core.audit import record_audit
from app.core.entitlements import CurrentUser
from app.domains.me.schemas import EntitlementsResponse


async def get_entitlements(session: AsyncSession, user: CurrentUser) -> EntitlementsResponse:
    scope_size = await session.scalar(
        select(func.count()).select_from(Account).where(scope_filter(user.access_scope))
    )
    # The web app asks once per page load, so this doubles as the sign-in record.
    record_audit(session, user, "sign_in")
    await session.commit()
    return EntitlementsResponse(
        upn=user.upn,
        name=user.name,
        role=user.role,
        data_scope=user.data_scope,
        permissions=sorted(user.permissions),
        scope_size=scope_size or 0,
    )
