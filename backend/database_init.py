import os
import time
from sqlmodel import SQLModel
from sqlalchemy import create_engine, inspect
from src.config import settings

def initialize_database():
    """Initialize the database with proper error handling and retries"""
    print("Initializing database...")

    # Use the same engine creation logic as in session.py but without problematic params
    if settings.database_url.startswith("postgresql"):
        # For PostgreSQL/Neon, create engine without problematic command_timeout
        engine = create_engine(
            settings.database_url,
            echo=settings.db_echo,
            connect_args={
                "connect_timeout": 10,
                # Remove command_timeout as it's not supported by psycopg2
            }
        )
    else:
        # For SQLite
        engine = create_engine(
            settings.database_url,
            echo=settings.db_echo,
            connect_args={
                "check_same_thread": False
            }
        )

    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            print(f"Attempt {retry_count + 1} to connect to database...")

            # Test the connection first
            from sqlalchemy import text
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("Database connection successful!")

            # Check if tables exist
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()

            print(f"Existing tables: {existing_tables}")

            # Create all tables if they don't exist
            if not existing_tables:
                print("No tables found, creating all tables...")
                SQLModel.metadata.create_all(bind=engine)
                print("All tables created successfully!")
            else:
                print("Tables already exist.")

            return True

        except Exception as e:
            print(f"Database initialization attempt {retry_count + 1} failed: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Failed to initialize database after {max_retries} attempts")
                raise e

if __name__ == "__main__":
    initialize_database()