from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """OS environment variables take precedence over the local .env file."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        str_strip_whitespace=True,
    )

    app_name: str = Field(default="Event Ticketing API", min_length=1)
    app_version: str = Field(default="1.0.0", min_length=1)
    app_env: Literal["development", "test", "production"] = "development"
    http_host: str = Field(default="127.0.0.1", min_length=1)
    http_port: int = Field(default=8000, ge=1, le=65535)
