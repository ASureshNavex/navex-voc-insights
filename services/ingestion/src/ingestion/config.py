from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    database_url: str = "postgresql+asyncpg://voc:voc@localhost:5432/voc"
    aws_region: str = "us-west-2"

    snowflake_account: str = ""
    snowflake_user: str = ""
    snowflake_private_key_secret: str = ""
    snowflake_warehouse: str = ""
    snowflake_account_view: str = ""

    enterpret_mcp_url: str = ""
    enterpret_token_secret: str = ""
    scoring_window_days: int = 90

    scoring_agent_runtime_arn: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
