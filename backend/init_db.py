import os
import sys
# Add backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set the database URL to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:///./todo_app_hf.db'

from sqlmodel import SQLModel
from sqlalchemy import create_engine
from src.database.session import get_engine
from src.models.user import User
from src.models.todo import Todo
from src.models.profile import UserProfile

print("Initializing database tables...")

try:
    # Get the engine
    engine = get_engine()

    # Create all tables
    SQLModel.metadata.create_all(bind=engine)

    print("Database tables created successfully!")

    # Check if tables exist by counting users
    from sqlalchemy.sql import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Tables in database: {tables}")

except Exception as e:
    print(f"Error initializing database: {e}")
    import traceback
    traceback.print_exc()