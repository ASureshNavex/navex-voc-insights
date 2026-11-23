from pydantic import BaseModel
from voc_data.enums import DataScope, Role


class EntitlementsResponse(BaseModel):
    upn: str
    name: str
    role: Role
    data_scope: DataScope
    permissions: list[str]
    scope_size: int
