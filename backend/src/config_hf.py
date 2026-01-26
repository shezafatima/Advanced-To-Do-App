from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # Database settings - default to SQLite for Hugging Face deployment
    database_url: str = "sqlite:///./todo_app_hf.db"
    db_echo: bool = False  # Set to True to log SQL queries

    # JWT settings
    secret_key: str = "your-secret-key-here-32-characters-at-least"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours as specified in clarifications

    # Allow override via environment variable
    neon_database_url: Optional[str] = None


# Override database_url if DATABASE_URL environment variable is set
if os.getenv('DATABASE_URL'):
    # If DATABASE_URL is set via environment, use it
    temp_settings = Settings()
    temp_settings.database_url = os.getenv('DATABASE_URL', temp_settings.database_url)
    settings = temp_settings
else:
    # Otherwise, use the default (SQLite)
    settings = Settings()