from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify system health check endpoint returns 200 and expected schema."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Advanced Shawl Draping Renders"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data
    assert "items_loaded" in data
    assert data["render_engine"] == "OptiX Ray-Tracing / Cloth Physics 2.4"


def test_analytics_metrics_endpoint():
    """Verify analytics metrics endpoint returns status 200 with aggregated simulation data."""
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_renders" in data
    assert "average_score" in data
    assert "status_breakdown" in data
    assert "current_theme_config" in data
    assert "score_distribution" in data
    assert "recent_activity" in data
    assert isinstance(data["total_renders"], int)
    assert isinstance(data["average_score"], float)
    assert isinstance(data["status_breakdown"], dict)
    assert isinstance(data["score_distribution"], list)
    assert len(data["recent_activity"]) > 0


def test_post_review_valid():
    """Verify successful submission of review and quality classification."""
    payload = {
        "title": "Tussar Silk Embroidered Shawl - Pleated Fold",
        "status": "approved",
        "score": 94.5,
        "theme_config": {
            "lighting_intensity": 1.6,
            "background_theme": "dark-velvet",
            "accent_color": "#F4C430",
            "hdri_environment": "atelier_warm_highbay"
        }
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "approved"
    assert data["score"] == 94.5
    assert "id" in data
    assert "timestamp" in data
    assert data["theme_config"]["background_theme"] == "dark-velvet"
    assert data["theme_config"]["lighting_intensity"] == 1.6


def test_post_review_invalid_status():
    """Verify validation failure when submitting an unaccepted drape status."""
    payload = {
        "title": "Invalid Status Drape Test",
        "status": "non-existent-status",
        "score": 85.0
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 422


def test_update_render_config():
    """Verify updating render lighting and backdrop theme parameters."""
    config_payload = {
        "lighting_intensity": 2.25,
        "background_theme": "slate-noir",
        "accent_color": "#00FFCC",
        "hdri_environment": "studio_softbox_4k"
    }
    response = client.post("/api/render/config", json=config_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["lighting_intensity"] == 2.25
    assert data["background_theme"] == "slate-noir"
    assert data["accent_color"] == "#00FFCC"
    assert data["hdri_environment"] == "studio_softbox_4k"
