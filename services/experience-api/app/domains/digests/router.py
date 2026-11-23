from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.entitlements import CurrentUser, require_permission
from app.core.exceptions import NotBuilt
from app.core.pagination import Page, PageParams, page_params
from app.domains.digests.schemas import (
    ArchivedDigest,
    DigestPreference,
    DigestPreview,
    DigestResponse,
    DigestUpdate,
)

router = APIRouter(tags=["digests"])

Manager = Annotated[CurrentUser, Depends(require_permission("digests:manage"))]
Subscriber = Annotated[CurrentUser, Depends(require_permission("digest_preferences:manage"))]
Paging = Annotated[PageParams, Depends(page_params)]


@router.get("/admin/digests")
async def list_digests(user: Manager, page: Paging) -> Page[DigestResponse]:
    raise NotBuilt("DIG-01: digest schedules.")


@router.patch("/admin/digests/{digest_id}")
async def update_digest(digest_id: UUID, user: Manager, body: DigestUpdate) -> DigestResponse:
    raise NotBuilt("DIG-03: configure schedule, content, pause and resume.")


@router.post("/admin/digests/{digest_id}/preview")
async def preview_digest(digest_id: UUID, user: Manager) -> DigestPreview:
    raise NotBuilt("DIG-04: preview as a recipient sees it.")


@router.post("/admin/digests/{digest_id}/send", status_code=status.HTTP_202_ACCEPTED)
async def send_digest_now(digest_id: UUID, user: Manager) -> None:
    raise NotBuilt("DIG-04: queue the digest for the notification task.")


@router.get("/admin/digests/archive")
async def list_archive(user: Manager, page: Paging) -> Page[ArchivedDigest]:
    raise NotBuilt("DIG-05: digests sent in the last 30 days.")


@router.get("/me/digest-preferences")
async def get_preferences(user: Subscriber) -> list[DigestPreference]:
    raise NotBuilt("DIG-07: personal digest settings.")


@router.put("/me/digest-preferences")
async def put_preferences(user: Subscriber, body: list[DigestPreference]) -> list[DigestPreference]:
    raise NotBuilt("DIG-07: personal digest settings.")
