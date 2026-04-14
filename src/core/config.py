from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    APP_NAME: str = Field(
        default="Robo Call Service",
        description="Service name shown in OpenAPI and logs.",
    )
    APP_VERSION: str = Field(default="0.1.0", description="Service semver.")
    APP_ENV: Literal["development", "staging", "production"] = Field(
        default="development", description="Deployment environment."
    )
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="Python logging level."
    )

    HOST: str = Field(default="0.0.0.0", description="Uvicorn bind host.")
    PORT: int = Field(default=8000, ge=1, le=65535, description="Uvicorn bind port.")

    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed CORS origins as a JSON list.",
    )
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=30, ge=1, description="Per-IP requests-per-minute cap."
    )

    TWILIO_ACCOUNT_SID: str = Field(
        ..., min_length=10, description="Twilio Account SID (starts with 'AC')."
    )
    TWILIO_AUTH_TOKEN: str = Field(
        ..., min_length=10, description="Twilio Auth Token."
    )
    TWILIO_FROM_NUMBER: str = Field(
        ...,
        pattern=r"^\+[1-9]\d{1,14}$",
        description="Twilio outbound caller ID in E.164 format (e.g. +18339213517).",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
