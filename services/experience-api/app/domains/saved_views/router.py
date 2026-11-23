from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.entitlements import CurrentUser, require_permission
from app.core.pagination import PageParams, page_params
from app.domains.saved_views import service
from app.domains.saved_views.schemas import SavedViewCreate, SavedViewRename, SavedViewResponse

router = APIRouter(prefix="/saved-views", tags=["saved views"])

Owner = Annotated[CurrentUser, Depends(require_permission("saved_views:manage"))]
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("")
async def list_views(
    user: Owner, session: Session, page: Annotated[PageParams, Depends(page_params)]
) -> list[SavedViewResponse]:
    return await service.list_views(session, user, page)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_view(user: Owner, session: Session, body: SavedViewCreate) -> SavedViewResponse:
    return await service.create_view(session, user, body)


@router.patch("/{view_id}")
async def rename_view(
    view_id: UUID, user: Owner, session: Session, body: SavedViewRename
) -> SavedViewResponse:
    return await service.rename_view(session, user, view_id, body.name)


@router.delete("/{view_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_view(view_id: UUID, user: Owner, session: Session) -> None:
    await service.delete_view(session, user, view_id)
