"""Application configuration loaded from the project's .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


class Settings(BaseSettings):
    """Validated settings shared by the backend application."""

    gemini_api_key: str = Field(min_length=1)
    groq_api_key: str = Field(min_length=1)
    database_url: str = Field(min_length=1)
    log_level: str = Field(min_length=1)
    secret_key: str = Field(min_length=32)
    model_name: str = Field(min_length=1)
    default_llm_provider: str = Field(default="gemini", pattern="^(gemini|groq)$")
    gemini_model: str = Field(default="gemini-3.6-flash", min_length=1)
    groq_model: str = Field(default="llama-3.3-70b-versatile", min_length=1)
    llm_timeout_seconds: float = Field(default=60.0, gt=0, le=300)
    embedding_model: str = Field(min_length=1)
    chroma_path: str = Field(min_length=1)
    embedding_batch_size: int = Field(default=50, ge=1, le=100)
    embedding_batch_pause_seconds: float = Field(default=30.0, ge=0)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        """Require SQLite and resolve relative database files from backend/ consistently."""
        if not value.startswith("sqlite:///"):
            raise ValueError("DATABASE_URL must start with 'sqlite:///'")

        database_path = value.removeprefix("sqlite:///")
        if database_path.startswith("./"):
            resolved_path = PROJECT_ROOT / "backend" / database_path.removeprefix("./")
            return f"sqlite:///{resolved_path.as_posix()}"
        return value

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Normalize and validate the configured logging level."""
        normalized_value = value.upper()
        if normalized_value not in VALID_LOG_LEVELS:
            allowed_levels = ", ".join(sorted(VALID_LOG_LEVELS))
            raise ValueError(f"LOG_LEVEL must be one of: {allowed_levels}")
        return normalized_value

    @field_validator("chroma_path")
    @classmethod
    def validate_chroma_path(cls, value: str) -> str:
        """Resolve persistent Chroma storage relative to backend/ when configured with ./ syntax."""
        path = Path(value)
        if not path.is_absolute():
            path = PROJECT_ROOT / "backend" / path
        return str(path.resolve())


@lru_cache
def get_settings() -> Settings:
    """Load and cache application settings after validating environment values."""
    return Settings()


def validate_settings() -> Settings:
    """Validate settings during application startup and return them."""
    return get_settings()
