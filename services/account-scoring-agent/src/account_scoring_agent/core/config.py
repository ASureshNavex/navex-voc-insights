from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_RULES_DIR = Path(__file__).resolve().parent.parent / "rules"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    database_url: str = "postgresql+asyncpg://voc:voc@localhost:5432/voc"
    aws_region: str = "us-west-2"

    bedrock_model_id: str = ""
    bedrock_timeout_seconds: int = 60
    summary_concurrency: int = 4

    rule_set_path: Path = _RULES_DIR / "placeholder-v0.yaml"
    confirm_runs: int = 2
    driver_verbatims_per_theme: int = 2

    event_bus_name: str = "default"


@lru_cache
def get_settings() -> Settings:
    return Settings()
