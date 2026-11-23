from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.entitlements import CurrentUser, get_current_user
from app.domains.me import service
from app.domains.me.schemas import EntitlementsResponse

router = APIRouter(prefix="/me", tags=["me"])


@router.get("/entitlements")
async def read_entitlements(
    user: Annotated[CurrentUser, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EntitlementsResponse:
    return await service.get_entitlements(session, user)
