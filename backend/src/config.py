from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # Database settings
    database_url: str = "postgresql://username:password@localhost:5432/todo_app"
    db_echo: bool = False  # Set to True to log SQL queries

    # JWT settings
    secret_key: str = "your-secret-key-here-32-characters-at-least"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours as specified in clarifications

    # Neon settings
    neon_database_url: Optional[str] = None


settings = Settings()