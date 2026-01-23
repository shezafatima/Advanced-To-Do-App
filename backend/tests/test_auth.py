"""
Authentication tests for the Todo Full-Stack Web Application.

This module tests all authentication-related functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.models.user import User


def test_register_new_user(client: TestClient, session: Session):
    """Test registering a new user."""
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "SecurePassword123!"
    })

    assert response.status_code == 200

    # Verify user was created in database
    user = session.query(User).filter(User.email == "newuser@example.com").first()
    assert user is not None
    assert user.email == "newuser@example.com"
    assert user.is_active is True


def test_register_duplicate_email(client: TestClient):
    """Test registering a user with an existing email."""
    # First registration should succeed
    first_response = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "SecurePassword123!"
    })
    assert first_response.status_code == 200

    # Second registration with same email should fail
    second_response = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "AnotherPassword456!"
    })
    assert second_response.status_code == 400  # Or 409 depending on implementation


def test_login_valid_credentials(client: TestClient, test_user: User):
    """Test logging in with valid credentials."""
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "TestPassword123!"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test logging in with invalid credentials."""
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "WrongPassword123!"
    })

    assert response.status_code == 401


def test_get_current_user_authenticated(authenticated_client: TestClient, test_user: User):
    """Test getting current user info when authenticated."""
    response = authenticated_client.get("/auth/me")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["id"] == str(test_user.id)


def test_get_current_user_unauthenticated(client: TestClient):
    """Test getting current user info when not authenticated."""
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_password_validation_on_registration(client: TestClient):
    """Test that passwords are properly validated during registration."""
    # Test weak password (too short)
    response = client.post("/auth/register", json={
        "email": "weakpass@example.com",
        "password": "weak"
    })
    assert response.status_code != 200  # Should fail validation

    # Test strong password
    response = client.post("/auth/register", json={
        "email": "strongpass@example.com",
        "password": "StrongPassword123!"
    })
    assert response.status_code == 200