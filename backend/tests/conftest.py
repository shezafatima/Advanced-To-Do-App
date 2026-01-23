"""
Pytest configuration for the Todo Full-Stack Web Application backend tests.

This module sets up test fixtures and configurations for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.main import app
from src.database.session import get_session, engine
from src.models.user import User
from src.models.todo import Todo


@pytest.fixture(name="engine")
def fixture_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(name="session")
def fixture_session(engine):
    """Create a test database session."""
    from sqlmodel import Session

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def fixture_client(session):
    """Create a test client with dependency overrides."""

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session):
    """Create a test user."""
    from werkzeug.security import generate_password_hash

    user = User(
        email="test@example.com",
        hashed_password=generate_password_hash("TestPassword123!"),
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def authenticated_client(client, test_user):
    """Create an authenticated test client."""
    # Login to get token
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "TestPassword123!"
    })
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]

    # Set authorization header for subsequent requests
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client