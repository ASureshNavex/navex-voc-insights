from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.entitlements import CurrentUser, require_permission
from app.core.exceptions import NotBuilt
from app.core.pagination import Page, PageParams, page_params
from app.domains.knowledge_hub.schemas import (
    DeclineRequest,
    DocumentResponse,
    DownloadLink,
    UploadRequest,
    UploadTicket,
)

router = APIRouter(prefix="/knowledge-hub", tags=["knowledge hub"])

Uploader = Annotated[CurrentUser, Depends(require_permission("knowledge_hub:upload"))]
Approver = Annotated[CurrentUser, Depends(require_permission("knowledge_hub:approve"))]


@router.post("/uploads", status_code=status.HTTP_201_CREATED)
async def request_upload(user: Uploader, body: UploadRequest) -> UploadTicket:
    raise NotBuilt("KHB-01: create the record and return a presigned upload URL.")


@router.post("/files/{document_id}/complete")
async def complete_upload(document_id: UUID, user: Uploader) -> DocumentResponse:
    raise NotBuilt("KHB-02: mark the upload finished and start file checks.")


@router.get("/files")
async def list_files(
    user: Uploader, page: Annotated[PageParams, Depends(page_params)]
) -> Page[DocumentResponse]:
    raise NotBuilt("KHB-03: uploads list.")


@router.get("/files/{document_id}/download")
async def download_file(document_id: UUID, user: Uploader) -> DownloadLink:
    raise NotBuilt("KHB-03: presigned download URL after a scope check.")


@router.delete("/files/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_file(document_id: UUID, user: Uploader) -> None:
    raise NotBuilt("KHB-04: withdraw a file.")


@router.post("/files/{document_id}/approve")
async def approve_file(document_id: UUID, user: Approver) -> DocumentResponse:
    raise NotBuilt("KHB-04: publish a file that is awaiting approval.")


@router.post("/files/{document_id}/decline")
async def decline_file(document_id: UUID, user: Approver, body: DeclineRequest) -> DocumentResponse:
    raise NotBuilt("KHB-04: decline with a reason.")
