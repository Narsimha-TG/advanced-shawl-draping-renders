import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_hotels():
    response = client.get("/api/v1/hotels")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_reservation_success():
    payload = {
        "property_id": "1",
        "check_in_date": "2023-12-01",
        "check_out_date": "2023-12-05",
        "guest_details": {"name": "John Doe", "email": "john@example.com"}
    }
    response = client.post("/api/v1/reservations", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()

def test_process_payment():
    payload = {"reservation_id": "test-id", "amount": 1200}
    response = client.post("/api/v1/payments/process", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_nonexistent_reservation():
    response = client.get("/api/v1/reservations/invalid-uuid")
    assert response.status_code == 404