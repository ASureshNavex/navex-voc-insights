from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from voc_data.enums import DataScope, Role


class RoleMapping(BaseModel):
    role: Role
    scope: DataScope


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    database_url: str = "postgresql+asyncpg://voc:voc@localhost:5432/voc"
    aws_region: str = "us-west-2"

    entra_tenant_id: str = ""
    entra_api_audience: str = ""
    # Corp AD app role value or group object ID -> platform role and data scope.
    voc_role_map: dict[str, RoleMapping] = {}

    documents_bucket: str = ""
    knowledge_hub_require_approval: bool = False
    knowledge_hub_max_bytes: int = 25 * 1024 * 1024

    otel_enabled: bool = False
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
