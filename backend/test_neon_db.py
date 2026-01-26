import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set the database URL to use Neon PostgreSQL
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_HhXVdL2K5Gmx@ep-calm-fog-ah0itwx9-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

from sqlmodel import SQLModel
from sqlalchemy import text
from src.database.session import get_engine
from src.models.user import User
from src.models.todo import Todo
from src.models.profile import UserProfile

print("Testing connection to Neon PostgreSQL...")

try:
    # Get the engine
    engine = get_engine()

    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connection successful! Test query returned:", result.fetchone())

    # Create all tables (this will work if the connection is valid)
    print("Creating tables in Neon PostgreSQL...")
    SQLModel.metadata.create_all(bind=engine)

    print("Tables created successfully in Neon PostgreSQL!")

    # Check what tables exist
    with engine.connect() as conn:
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Tables in Neon database: {tables}")

except Exception as e:
    print(f"Error connecting to Neon PostgreSQL: {e}")
    import traceback
    traceback.print_exc()