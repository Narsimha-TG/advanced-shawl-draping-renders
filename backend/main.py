from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI(title="Descriptif Produit Formel Persuasif API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductReview(BaseModel):
    id: str = None
    title: str
    status: str
    score: float
    timestamp: str = None

# In-memory seed data
db = [
    {"id": "1", "title": "Premium Wireless Headphones", "status": "active", "score": 4.8, "timestamp": "2023-10-27T10:00:00Z"},
    {"id": "2", "title": "Ergonomic Office Chair", "status": "pending", "score": 4.2, "timestamp": "2023-10-27T11:30:00Z"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    avg_score = sum(item["score"] for item in db) / len(db) if db else 0
    return {"total_items": len(db), "average_score": avg_score}

@app.post("/api/reviews", response_model=ProductReview)
def create_review(review: ProductReview):
    review.id = str(uuid.uuid4())
    review.timestamp = datetime.utcnow().isoformat()
    db.append(review.dict())
    return review

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)