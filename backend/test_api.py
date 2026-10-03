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
    assert "total_orders" in response.json()
    assert "active_fabrication" in response.json()

def test_submit_order():
    payload = {
        "cad_file_hash": "a1b2c3d4e5f6",
        "material_spec": "ASTM A513",
        "tolerance_threshold": 0.005,
        "budget_allocation": 1500.00
    }
    response = client.post("/api/orders/submit", json=payload)
    assert response.status_code == 201
    assert "order_id" in response.json()
    assert response.json()["message"] == "Order submitted successfully"

def test_get_order_status_not_found():
    response = client.get("/api/orders/non-existent-id/status")
    assert response.status_code == 404