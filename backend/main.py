from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="2D Animated Product Video API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int
    title: str
    status: str
    score: float
    timestamp: str
    theme_preference: str = "light"

# In-memory seed data
db = [
    {"id": 1, "title": "Intro Animation", "status": "completed", "score": 9.5, "timestamp": "2023-10-27T10:00:00Z", "theme_preference": "light"},
    {"id": 2, "title": "Product Showcase", "status": "in-progress", "score": 8.2, "timestamp": "2023-10-27T11:30:00Z", "theme_preference": "dark"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_items": len(db), "average_score": sum(item['score'] for item in db) / len(db) if db else 0}

@app.post("/api/reviews")
def create_review(review: Review):
    db.append(review.dict())
    return review

@app.patch("/api/theme")
def update_theme(theme: str):
    if theme not in ["light", "dark"]:
        raise HTTPException(status_code=400, detail="Invalid theme")
    return {"message": f"Theme updated to {theme}"}
