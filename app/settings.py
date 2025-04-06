from decimal import Decimal
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    NAME: str = "Tokoff Chain"

    HOST: str = Field(default="localhost")
    PORT: int = Field(default=8000, gt=0, le=65535)
    ENVIRONMENT: Literal["development", "production"] = Field(
        default="development",
    )
    DEBUG: bool = Field(default=False)

    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="postgres")
    DB_HOST: str = Field(default="localhost")
    DB_NAME: str = Field(default="development")
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    NUMBER_PRECISION: int = 18
    NUMBER_SCALE: int = 6
    MIN_TRANSACTION_SIZE: Decimal = Decimal(1) / Decimal(NUMBER_SCALE)
    MAX_TRANSACTION_SIZE: Decimal = Decimal(999) * Decimal(
        NUMBER_PRECISION / NUMBER_SCALE,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )


settings = Settings()

if settings.ENVIRONMENT == "development":
    settings.DEBUG = True
