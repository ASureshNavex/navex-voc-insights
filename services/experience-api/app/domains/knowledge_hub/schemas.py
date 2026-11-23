from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from voc_data.enums import DocumentStatus


class UploadRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    file_name: str = Field(min_length=1, max_length=255)
    content_type: str
    size_bytes: int = Field(gt=0)
    product_domain: str | None = None


class UploadTicket(BaseModel):
    document_id: UUID
    upload_url: str
    expires_in_seconds: int


class DocumentResponse(BaseModel):
    document_id: UUID
    title: str
    file_name: str
    product_domain: str | None
    size_bytes: int
    uploaded_by: str
    uploaded_at: datetime
    status: DocumentStatus
    decline_reason: str | None


class DeclineRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


class DownloadLink(BaseModel):
    url: str
    expires_in_seconds: int
