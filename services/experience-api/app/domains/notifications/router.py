from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.entitlements import CurrentUser, require_permission
from app.core.exceptions import NotBuilt
from app.core.pagination import PageParams, page_params
from app.domains.notifications.schemas import NotificationList

router = APIRouter(prefix="/notifications", tags=["notifications"])

Reader = Annotated[CurrentUser, Depends(require_permission("notifications:read"))]


@router.get("")
async def list_notifications(
    user: Reader, page: Annotated[PageParams, Depends(page_params)]
) -> NotificationList:
    raise NotBuilt("ALR-05: notifications for the bell icon, newest first.")


@router.post("/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_read(user: Reader) -> None:
    raise NotBuilt("ALR-05: mark the caller's notifications read.")
