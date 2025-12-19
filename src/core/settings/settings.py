from functools import lru_cache
from typing import Any

from pydantic import AnyHttpUrl, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class EnvironmentSettings(BaseSettings):
    API_PREFIX: str = "/api"
    API_TITLE: str
    APP_PORT: int | str
    CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    LOG_LEVEL: str
    PROFILING_ENABLED: bool

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int | str
    DATABASE_NAME: str

    SQLALCHEMY_ECHO: bool
    SQLALCHEMY_ISOLATION_LEVEL: str
    DB_POOL_SIZE: int = 90
    MAX_OVERFLOW: int = 64
    ASYNC_DATABASE_URI: PostgresDsn | None = None

    SESSION_EXPIRES_IN: int
    SESSION_SECRET_KEY: str
    USE_SECURE_COOKIES: bool = True

    @field_validator("ASYNC_DATABASE_URI")
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("DATABASE_USER"),
            password=values.data.get("DATABASE_PASSWORD"),
            host=values.data.get("DATABASE_HOST"),
            port=int(values.data.get("DATABASE_PORT")),
            path=f"{values.data.get('DATABASE_NAME') or ''}",
        )

    @field_validator("CORS_ORIGINS", mode="before")
    def _parse_cors_origins(cls, v):
        if isinstance(v, str):
            items = [item.strip() for item in v.split(",") if item.strip()]
            return items
        if isinstance(v, list):
            return v
        raise ValueError(f"CORS_ORIGINS must be a string, got {type(v)}: {v!r}")

    class Config:
        env_file = ".env"
        case_sensitive = True
        validate_assignment = True


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()


settings = get_environment_variables()
