from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)

class ThemeConfig(BaseModel):
    button_id: str
    hex_color_code: str
    hover_state_color: str
    section_anchor: str
    is_active: bool

class LeadCapture(BaseModel):
    name: str
    email: str
    property_interest: str

# In-memory seed data
theme_db = {
    "primary": {"button_id": "primary", "hex_color_code": "#0056b3", "hover_state_color": "#004494", "section_anchor": "#contact", "is_active": True}
}

@app.get("/api/v1/site-config")
def get_site_config():
    return list(theme_db.values())

@app.post("/api/v1/lead-capture")
def capture_lead(lead: LeadCapture):
    # Logic to process lead (e.g., send email or save to DB)
    return {"status": "success", "message": "Lead captured successfully"}

@app.patch("/api/v1/ui-theme")
def update_theme(config: ThemeConfig):
    if config.button_id not in theme_db:
        raise HTTPException(status_code=404, detail="Button ID not found")
    theme_db[config.button_id] = config
    return {"status": "updated", "data": config}
