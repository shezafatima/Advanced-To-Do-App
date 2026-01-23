"""Script to run database migrations"""
import asyncio
import os
from alembic.config import Config
from alembic import command
from pathlib import Path

def run_migrations():
    # Change to the backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    # Configure alembic
    alembic_cfg = Config("migrations/alembic.ini")

    # Set the script location
    alembic_cfg.set_main_option("script_location", "migrations")

    # Run the upgrade to head
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()