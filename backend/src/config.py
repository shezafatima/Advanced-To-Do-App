import os
from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')

    # Database settings
    database_url: str = "sqlite:///./todo_app_hf.db"  # Default to SQLite for Hugging Face
    db_echo: bool = False  # Set to True to log SQL queries

    # JWT settings
    secret_key: str = "your-secret-key-here-32-characters-at-least"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours as specified in clarifications

    # Neon settings
    neon_database_url: Optional[str] = None


# Override with environment variable if provided
if os.getenv('DATABASE_URL'):
    # Create temporary settings and override the database_url
    import os
    temp_database_url = os.getenv('DATABASE_URL')
    settings = Settings(database_url=temp_database_url)
else:
    settings = Settings()