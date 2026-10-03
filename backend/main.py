from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import uuid
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Advanced Shawl Draping Renders Microservice",
    description="Backend API for 3D shawl draping simulation metrics, quality reviews, and photorealistic lighting/render configurations.",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ThemeConfig(BaseModel):
    lighting_intensity: float = Field(
        default=1.2,
        ge=0.0,
        le=5.0,
        description="Fabric key light intensity multiplier (0.0 to 5.0)",
    )
    background_theme: str = Field(
        default="dark-velvet",
        description="Background preset: dark-velvet, slate-noir, studio-monochrome, or raw-atelier",
    )
    accent_color: str = Field(
        default="#E0A96D",
        description="Hex color for fabric specular rim highlights",
    )
    hdri_environment: str = Field(
        default="studio_softbox_4k",
        description="HDRI environment map identifier",
    )


class RenderItem(BaseModel):
    id: str
    title: str
    status: str = Field(..., description="Status: pending, approved, rejected, re-render")
    score: float = Field(..., ge=0.0, le=100.0, description="Fidelity/Drape realism score")
    timestamp: str
    theme_config: ThemeConfig


class ReviewCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    status: str = Field(default="approved", description="approved, rejected, or re-render")
    score: float = Field(..., ge=0.0, le=100.0)
    theme_config: Optional[ThemeConfig] = None


class RenderConfigUpdateRequest(BaseModel):
    lighting_intensity: float = Field(..., ge=0.0, le=5.0)
    background_theme: str
    accent_color: Optional[str] = "#E0A96D"
    hdri_environment: Optional[str] = "studio_softbox_4k"


class AnalyticsResponse(BaseModel):
    total_renders: int
    average_score: float
    status_breakdown: Dict[str, int]
    current_theme_config: ThemeConfig
    score_distribution: List[Dict[str, Any]]
    recent_activity: List[RenderItem]


# In-memory storage with production-style seed data
active_theme_config = ThemeConfig(
    lighting_intensity=1.45,
    background_theme="dark-velvet",
    accent_color="#F4C430",
    hdri_environment="atelier_warm_highbay"
)

renders_db: List[RenderItem] = [
    RenderItem(
        id="rnd-001",
        title="Kashmiri Pashmina - Asymmetric Shoulder Drape",
        status="approved",
        score=96.4,
        timestamp="2025-02-23T10:14:00Z",
        theme_config=ThemeConfig(lighting_intensity=1.5, background_theme="dark-velvet", accent_color="#F4C430", hdri_environment="atelier_warm_highbay"),
    ),
    RenderItem(
        id="rnd-002",
        title="Raw Silk Jamawar - Dynamic Gravity Fold",
        status="approved",
        score=92.1,
        timestamp="2025-02-23T11:42:00Z",
        theme_config=ThemeConfig(lighting_intensity=1.3, background_theme="slate-noir", accent_color="#E0A96D", hdri_environment="studio_softbox_4k"),
    ),
    RenderItem(
        id="rnd-003",
        title="Merino Wool Waterfall Wrap - Low Tension",
        status="re-render",
        score=74.8,
        timestamp="2025-02-23T13:05:00Z",
        theme_config=ThemeConfig(lighting_intensity=1.1, background_theme="raw-atelier", accent_color="#D4AF37", hdri_environment="cyclorama_dim"),
    ),
    RenderItem(
        id="rnd-004",
        title="Zari Brocade Stole - High Specular Highlight",
        status="rejected",
        score=58.2,
        timestamp="2025-02-23T14:20:00Z",
        theme_config=ThemeConfig(lighting_intensity=2.2, background_theme="studio-monochrome", accent_color="#FFD700", hdri_environment="harsh_spotlight"),
    ),
    RenderItem(
        id="rnd-005",
        title="Chiffon Ombre Wrap - Micro Wrinkle Collision",
        status="approved",
        score=89.7,
        timestamp="2025-02-23T15:33:00Z",
        theme_config=ThemeConfig(lighting_intensity=1.45, background_theme="dark-velvet", accent_color="#F4C430", hdri_environment="atelier_warm_highbay"),
    ),
]


@app.get("/api/health", tags=["System"])
def get_health() -> Dict[str, Any]:
    """System health, runtime state, and timestamp check."""
    return {
        "status": "healthy",
        "service": "Advanced Shawl Draping Renders",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "items_loaded": len(renders_db),
        "render_engine": "OptiX Ray-Tracing / Cloth Physics 2.4",
    }


@app.get("/api/analytics", response_model=AnalyticsResponse, tags=["Analytics"])
def get_analytics():
    """Aggregated metrics, scoring distribution, and fabric simulation performance data."""
    total = len(renders_db)
    avg_score = round(sum(r.score for r in renders_db) / total, 2) if total > 0 else 0.0

    breakdown: Dict[str, int] = {}
    for r in renders_db:
        breakdown[r.status] = breakdown.get(r.status, 0) + 1

    score_distribution = [
        {"range": "90-100 (Exceptional)", "count": len([r for r in renders_db if r.score >= 90])},
        {"range": "80-89 (Production Quality)", "count": len([r for r in renders_db if 80 <= r.score < 90])},
        {"range": "70-79 (Needs Refinement)", "count": len([r for r in renders_db if 70 <= r.score < 80])},
        {"range": "<70 (Failed Validation)", "count": len([r for r in renders_db if r.score < 70])},
    ]

    return AnalyticsResponse(
        total_renders=total,
        average_score=avg_score,
        status_breakdown=breakdown,
        current_theme_config=active_theme_config,
        score_distribution=score_distribution,
        recent_activity=list(reversed(renders_db[-10:])),
    )


@app.post("/api/reviews", response_model=RenderItem, status_code=status.HTTP_201_CREATED, tags=["Reviews"])
def submit_review(payload: ReviewCreateRequest):
    """Submit draping fidelity review, mesh QA classification, and theme snapshot."""
    valid_statuses = {"approved", "rejected", "re-render", "pending"}
    sanitized_status = payload.status.lower().strip()
    if sanitized_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status '{payload.status}'. Allowed options: {sorted(list(valid_statuses))}",
        )

    config_snapshot = payload.theme_config or active_theme_config
    new_item = RenderItem(
        id=f"rnd-{uuid.uuid4().hex[:6]}",
        title=payload.title,
        status=sanitized_status,
        score=round(payload.score, 1),
        timestamp=datetime.now(timezone.utc).isoformat(),
        theme_config=config_snapshot,
    )

    renders_db.append(new_item)
    return new_item


@app.post("/api/render/config", response_model=ThemeConfig, tags=["Render Configuration"])
def update_render_config(config_in: RenderConfigUpdateRequest):
    """Update lighting intensity, backdrop theme, and accent highlights for draping visualization."""
    global active_theme_config
    active_theme_config = ThemeConfig(
        lighting_intensity=round(config_in.lighting_intensity, 2),
        background_theme=config_in.background_theme,
        accent_color=config_in.accent_color or active_theme_config.accent_color,
        hdri_environment=config_in.hdri_environment or active_theme_config.hdri_environment,
    )
    return active_theme_config


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
