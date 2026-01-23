"""Script to create database migration"""
import os
from alembic.config import Config
from alembic import command
from pathlib import Path

def create_migration(message="Initial migration"):
    # Change to the backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    # Configure alembic
    alembic_cfg = Config("migrations/alembic.ini")

    # Set the script location
    alembic_cfg.set_main_option("script_location", "migrations")

    # Generate a new migration
    command.revision(alembic_cfg, message, autogenerate=True)

if __name__ == "__main__":
    import sys
    message = sys.argv[1] if len(sys.argv) > 1 else "Initial migration"
    create_migration(message)