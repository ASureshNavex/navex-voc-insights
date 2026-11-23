from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domains.accounts.schemas import AccountFilters


class SavedViewCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    filters: AccountFilters


class SavedViewRename(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class SavedViewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    view_id: UUID
    name: str
    filters: AccountFilters
    created_at: datetime
