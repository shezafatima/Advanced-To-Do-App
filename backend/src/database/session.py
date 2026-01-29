from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import QueuePool
from ..config import settings
import sqlite3
import contextlib
import asyncio
from sqlmodel import SQLModel

# Global variables to hold the engines (initialized to None)
_engine = None
_async_engine = None

def ensure_database_initialized(engine):
    """Ensure database tables are created"""
    from sqlalchemy import inspect
    try:
        # Check if tables exist first
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        # Create all tables if they don't exist
        if not existing_tables:  # Only create if no tables exist
            SQLModel.metadata.create_all(bind=engine)
        elif 'user' not in existing_tables:  # If critical tables are missing
            SQLModel.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Don't raise the exception to avoid blocking the request

def get_engine():
    """
    Get or create the database engine with appropriate configuration based on database type.
    This is lazy-loaded to avoid connection issues during import.
    """
    global _engine
    if _engine is None:
        if settings.database_url.startswith("sqlite"):
            # SQLite doesn't support connection timeout in connect_args
            _engine = create_engine(
                settings.database_url,
                echo=settings.db_echo,  # Set to True for debugging SQL queries
                connect_args={
                    "check_same_thread": False  # Required for SQLite thread safety
                }
            )
        else:
            # For PostgreSQL and other databases, use connection pooling
            # Neon-safe configuration
            _engine = create_engine(
                settings.database_url,
                echo=settings.db_echo,  # Set to True for debugging SQL queries
                poolclass=QueuePool,    # Use QueuePool for connection pooling
                pool_size=5,            # Reduced pool size for Railway
                max_overflow=10,        # Reduced overflow for Railway
                pool_pre_ping=True,     # Verify connections before use (Neon-safe)
                pool_recycle=300,       # Recycle connections every 5 minutes (Neon-safe)
                pool_timeout=10,        # Reduced timeout
                pool_reset_on_return='commit',  # Reset connection on return
                connect_args={
                    "connect_timeout": 5,   # Reduced timeout for Railway
                }
            )

        # Initialize database tables after engine creation
        ensure_database_initialized(_engine)

    return _engine


def get_async_engine():
    """
    Get or create the async database engine with appropriate configuration based on database type.
    This is lazy-loaded to avoid connection issues during import.
    """
    global _async_engine
    if _async_engine is None:
        if settings.database_url.startswith("sqlite"):
            # SQLite doesn't support connection timeout in connect_args
            _async_engine = create_async_engine(
                settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///"),
                echo=settings.db_echo,  # Set to True for debugging SQL queries
                connect_args={
                    "check_same_thread": False  # Required for SQLite thread safety
                }
            )
        else:
            # For PostgreSQL and other databases, use connection pooling
            # Neon-safe configuration
            _async_engine = create_async_engine(
                settings.database_url,
                echo=settings.db_echo,  # Set to True for debugging SQL queries
                poolclass=QueuePool,    # Use QueuePool for connection pooling
                pool_size=5,            # Reduced pool size for Railway
                max_overflow=10,        # Reduced overflow for Railway
                pool_pre_ping=True,     # Verify connections before use (Neon-safe)
                pool_recycle=300,       # Recycle connections every 5 minutes (Neon-safe)
                pool_timeout=10,        # Reduced timeout
                pool_reset_on_return='commit',  # Reset connection on return
                connect_args={
                    "connect_timeout": 5,   # Reduced timeout for Railway
                }
            )

    return _async_engine


def get_session():
    """
    Dependency to get a database session.
    """
    with Session(get_engine()) as session:
        yield session


@contextlib.asynccontextmanager
async def get_async_session():
    """
    Async context manager to get an async database session.
    """
    async with AsyncSession(get_async_engine()) as session:
        try:
            yield session
        finally:
            await session.close()


# For backward compatibility with sync operations
def get_session_context():
    """
    Context manager for sync sessions (using contextlib.contextmanager).
    """
    @contextlib.contextmanager
    def session_context():
        with Session(get_engine()) as session:
            yield session

    return session_context()