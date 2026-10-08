"""Tests for health check endpoint."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_check_returns_ok_status():
    """Health check endpoint should return status 'ok'."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
