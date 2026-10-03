import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_items" in data
    assert "average_score" in data
    assert isinstance(data["total_items"], int)

def test_create_review():
    payload = {
        "title": "Test Product",
        "status": "active",
        "score": 4.5
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Product"
    assert data["score"] == 4.5
    assert "id" in data
    assert "timestamp" in data