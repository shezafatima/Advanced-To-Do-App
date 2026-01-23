"""
Health check tests for the Todo Full-Stack Web Application.

This module tests all health check endpoints.
"""

from fastapi.testclient import TestClient


def test_ping_endpoint(client: TestClient):
    """Test the ping endpoint."""
    response = client.get("/health/ping")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "pong"


def test_basic_health_check(client: TestClient):
    """Test the basic health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]  # Could be degraded if checks fail
    assert "timestamp" in data
    assert "uptime" in data
    assert "checks" in data


def test_detailed_health_check(client: TestClient):
    """Test the detailed health check endpoint."""
    response = client.get("/health/detailed")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "timestamp" in data
    assert "version" in data
    assert "environment" in data
    assert "checks" in data
    assert "metrics" in data


def test_readiness_check(client: TestClient):
    """Test the readiness check endpoint."""
    response = client.get("/health/ready")

    # If all checks pass, should return 200; otherwise 503
    # For testing purposes, assuming the app is ready
    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert data["status"] == "ready"
        assert "timestamp" in data
        assert "checks" in data


def test_liveness_check(client: TestClient):
    """Test the liveness check endpoint."""
    response = client.get("/health/live")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data