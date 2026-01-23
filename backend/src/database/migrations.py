"""
Database migration utilities using Alembic
"""
from alembic import command
from alembic.config import Config
from pathlib import Path


def run_migrations():
    """
    Run database migrations using Alembic.
    """
    alembic_cfg = Config(str(Path(__file__).parent / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")


def create_migration(message: str):
    """
    Create a new migration using Alembic.
    """
    alembic_cfg = Config(str(Path(__file__).parent / "alembic.ini"))
    command.revision(alembic_cfg, message=message, autogenerate=True)