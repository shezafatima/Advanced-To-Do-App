"""
Todo functionality tests for the Todo Full-Stack Web Application.

This module tests all todo-related functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.models.user import User
from src.models.todo import Todo


def test_create_todo_authenticated(authenticated_client: TestClient):
    """Test creating a new todo when authenticated."""
    response = authenticated_client.post("/todos/", json={
        "title": "Test Todo",
        "description": "Test description"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test description"
    assert data["completed"] is False
    assert "id" in data
    assert "user_id" in data


def test_create_todo_unauthenticated(client: TestClient):
    """Test creating a todo when not authenticated."""
    response = client.post("/todos/", json={
        "title": "Test Todo",
        "description": "Test description"
    })

    assert response.status_code == 401


def test_get_todos_for_user(authenticated_client: TestClient, session: Session, test_user: User):
    """Test getting all todos for the authenticated user."""
    # Create a few todos for the user
    todo1 = Todo(title="Todo 1", description="First todo", user_id=test_user.id)
    todo2 = Todo(title="Todo 2", description="Second todo", user_id=test_user.id)
    session.add(todo1)
    session.add(todo2)
    session.commit()

    response = authenticated_client.get("/todos/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = [todo["title"] for todo in data]
    assert "Todo 1" in titles
    assert "Todo 2" in titles


def test_get_todos_unauthenticated(client: TestClient):
    """Test getting todos when not authenticated."""
    response = client.get("/todos/")

    assert response.status_code == 401


def test_get_specific_todo_authenticated(authenticated_client: TestClient, session: Session, test_user: User):
    """Test getting a specific todo when authenticated."""
    # Create a todo
    todo = Todo(title="Specific Todo", description="A specific todo", user_id=test_user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = authenticated_client.get(f"/todos/{todo.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(todo.id)
    assert data["title"] == "Specific Todo"


def test_get_specific_todo_unauthenticated(client: TestClient, session: Session, test_user: User):
    """Test getting a specific todo when not authenticated."""
    # Create a todo
    todo = Todo(title="Specific Todo", description="A specific todo", user_id=test_user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.get(f"/todos/{todo.id}")

    assert response.status_code == 401


def test_update_todo_authenticated(authenticated_client: TestClient, session: Session, test_user: User):
    """Test updating a todo when authenticated."""
    # Create a todo
    todo = Todo(title="Original Title", description="Original description", user_id=test_user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    # Update the todo
    response = authenticated_client.put(f"/todos/{todo.id}", json={
        "title": "Updated Title",
        "description": "Updated description",
        "completed": True
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    assert data["completed"] is True


def test_delete_todo_authenticated(authenticated_client: TestClient, session: Session, test_user: User):
    """Test deleting a todo when authenticated."""
    # Create a todo
    todo = Todo(title="Todo to Delete", description="Will be deleted", user_id=test_user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    # Delete the todo
    response = authenticated_client.delete(f"/todos/{todo.id}")

    assert response.status_code == 204

    # Verify the todo was deleted
    response = authenticated_client.get(f"/todos/{todo.id}")
    assert response.status_code == 404


def test_toggle_todo_completion(authenticated_client: TestClient, session: Session, test_user: User):
    """Test toggling a todo's completion status."""
    # Create a todo
    todo = Todo(title="Toggle Completion", description="Will toggle", user_id=test_user.id, completed=False)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    # Toggle completion to True
    response = authenticated_client.patch(f"/todos/{todo.id}/toggle", json={"completed": True})

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True

    # Toggle completion back to False
    response = authenticated_client.patch(f"/todos/{todo.id}/toggle", json={"completed": False})

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False


def test_user_data_isolation(authenticated_client: TestClient, session: Session, test_user: User):
    """Test that users can only access their own todos."""
    # Create another user
    other_user = User(
        email="other@example.com",
        hashed_password="other_password_hash",
        is_active=True
    )
    session.add(other_user)
    session.commit()
    session.refresh(other_user)

    # Create a todo for the other user
    other_todo = Todo(title="Other User's Todo", description="Private todo", user_id=other_user.id)
    session.add(other_todo)
    session.commit()
    session.refresh(other_todo)

    # Try to access other user's todo with current user's token
    response = authenticated_client.get(f"/todos/{other_todo.id}")

    # Should either return 404 (not found) or 403 (forbidden) depending on implementation
    # Both are acceptable for data isolation
    assert response.status_code in [404, 403]


def test_todo_validation(authenticated_client: TestClient):
    """Test that todos are properly validated."""
    # Test creating todo without title (should fail)
    response = authenticated_client.post("/todos/", json={
        "title": "",  # Empty title should fail validation
        "description": "Test description"
    })

    assert response.status_code == 422  # Validation error

    # Test creating todo with title exceeding max length (should fail)
    long_title = "A" * 501  # Exceeds 500 character limit
    response = authenticated_client.post("/todos/", json={
        "title": long_title,
        "description": "Test description"
    })

    assert response.status_code == 422  # Validation error