from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from voc_data.models import SavedView

from app.core.audit import record_audit
from app.core.entitlements import CurrentUser
from app.core.exceptions import Conflict, NotFound
from app.core.pagination import PageParams
from app.domains.saved_views.schemas import SavedViewCreate, SavedViewResponse

_DUPLICATE = "You already have a saved view with this name."


async def _own_view(session: AsyncSession, user: CurrentUser, view_id: UUID) -> SavedView:
    view = await session.scalar(
        select(SavedView).where(SavedView.view_id == view_id, SavedView.owner_upn == user.upn)
    )
    if view is None:
        raise NotFound("Saved view not found.")
    return view


async def _commit_unique(session: AsyncSession) -> None:
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise Conflict(_DUPLICATE) from exc


async def list_views(
    session: AsyncSession, user: CurrentUser, page: PageParams
) -> list[SavedViewResponse]:
    views = await session.scalars(
        select(SavedView)
        .where(SavedView.owner_upn == user.upn)
        .order_by(SavedView.name, SavedView.view_id)
        .limit(page.limit)
        .offset(page.offset)
    )
    return [SavedViewResponse.model_validate(view) for view in views]


async def create_view(
    session: AsyncSession, user: CurrentUser, body: SavedViewCreate
) -> SavedViewResponse:
    view = SavedView(
        owner_upn=user.upn, name=body.name.strip(), filters=body.filters.model_dump(mode="json")
    )
    session.add(view)
    record_audit(session, user, "saved_view_created", name=view.name)
    await _commit_unique(session)
    await session.refresh(view)
    return SavedViewResponse.model_validate(view)


async def rename_view(
    session: AsyncSession, user: CurrentUser, view_id: UUID, name: str
) -> SavedViewResponse:
    view = await _own_view(session, user, view_id)
    view.name = name.strip()
    await _commit_unique(session)
    await session.refresh(view)
    return SavedViewResponse.model_validate(view)


async def delete_view(session: AsyncSession, user: CurrentUser, view_id: UUID) -> None:
    view = await _own_view(session, user, view_id)
    await session.delete(view)
    await session.commit()
