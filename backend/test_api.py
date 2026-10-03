import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_site_config():
    response = client.get("/api/v1/site-config")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_lead_capture_success():
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "property_interest": "Luxury Villa"
    }
    response = client.post("/api/v1/lead-capture", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_patch_ui_theme_success():
    payload = {
        "button_id": "primary",
        "hex_color_code": "#ff0000",
        "hover_state_color": "#cc0000",
        "section_anchor": "#contact",
        "is_active": True
    }
    response = client.patch("/api/v1/ui-theme", json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["hex_color_code"] == "#ff0000"

def test_patch_ui_theme_not_found():
    payload = {
        "button_id": "non-existent",
        "hex_color_code": "#000000",
        "hover_state_color": "#000000",
        "section_anchor": "#",
        "is_active": True
    }
    response = client.patch("/api/v1/ui-theme", json=payload)
    assert response.status_code == 404