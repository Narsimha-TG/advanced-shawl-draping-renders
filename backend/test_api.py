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
        "id": 3,
        "title": "Test Animation",
        "status": "pending",
        "score": 9.0,
        "timestamp": "2023-10-27T12:00:00Z",
        "theme_preference": "dark"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json() == payload

def test_update_theme_invalid():
    response = client.patch("/api/theme?theme=neon")
    assert response.status_code == 400