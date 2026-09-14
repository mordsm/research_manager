from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RESEARCH_MANAGER_", env_file=".env", extra="ignore")

    database_path: Path = Field(default=Path("data/research_manager.db"))
    max_iterations: int = Field(default=2, ge=1, le=10)


@lru_cache
def get_settings() -> Settings:
    return Settings()

