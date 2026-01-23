from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import QueuePool
from ..config import settings
import sqlite3
import contextlib
import asyncio


def create_engine_with_fallback():
    """
    Create database engine with appropriate configuration based on database type.
    """
    if settings.database_url.startswith("sqlite"):
        # SQLite doesn't support connection timeout in connect_args
        return create_engine(
            settings.database_url,
            echo=settings.db_echo,  # Set to True for debugging SQL queries
            connect_args={
                "check_same_thread": False  # Required for SQLite thread safety
            }
        )
    else:
        # For PostgreSQL and other databases, use connection pooling
        return create_engine(
            settings.database_url,
            echo=settings.db_echo,  # Set to True for debugging SQL queries
            poolclass=QueuePool,    # Use QueuePool for connection pooling
            pool_size=10,           # Number of connections to maintain
            max_overflow=20,        # Additional connections beyond pool_size
            pool_pre_ping=True,     # Verify connections before use
            pool_recycle=300,       # Recycle connections every 5 minutes
            pool_timeout=30,        # Timeout for getting a connection from pool
            connect_args={
                "connect_timeout": 10  # Timeout for establishing connection
            }
        )


def create_async_engine_with_fallback():
    """
    Create async database engine with appropriate configuration based on database type.
    """
    if settings.database_url.startswith("sqlite"):
        # SQLite doesn't support connection timeout in connect_args
        return create_async_engine(
            settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///"),
            echo=settings.db_echo,  # Set to True for debugging SQL queries
            connect_args={
                "check_same_thread": False  # Required for SQLite thread safety
            }
        )
    else:
        # For PostgreSQL and other databases, use connection pooling
        return create_async_engine(
            settings.database_url,
            echo=settings.db_echo,  # Set to True for debugging SQL queries
            poolclass=QueuePool,    # Use QueuePool for connection pooling
            pool_size=10,           # Number of connections to maintain
            max_overflow=20,        # Additional connections beyond pool_size
            pool_pre_ping=True,     # Verify connections before use
            pool_recycle=300,       # Recycle connections every 5 minutes
            pool_timeout=30,        # Timeout for getting a connection from pool
            connect_args={
                "connect_timeout": 10  # Timeout for establishing connection
            }
        )


# Create the database engines with appropriate configuration
engine = create_engine_with_fallback()
async_engine = create_async_engine_with_fallback()


def get_session():
    """
    Dependency to get a database session.
    """
    with Session(engine) as session:
        yield session


@contextlib.asynccontextmanager
async def get_async_session():
    """
    Async context manager to get an async database session.
    """
    async with AsyncSession(async_engine) as session:
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
        with Session(engine) as session:
            yield session

    return session_context()