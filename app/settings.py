from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = Field(default="localhost")
    PORT: int = Field(default=8000, gt=0, le=65535)
    ENVIRONMENT: Literal["development", "production"] = Field(
        default="development",
    )
    MIN_TRANSACTION_SIZE: float = 0.000_001
    MAX_TRANSACTION_SIZE: float = 1_000_000_000_000

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        str_strip_whitespace=True,
    )


settings = Settings()
