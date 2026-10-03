from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Custom Welded Steel Tubing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cad_file_hash: str
    material_spec: str
    tolerance_threshold: float
    status: str = "Pending"
    budget_allocation: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# In-memory storage
db = []

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_orders": len(db), "active_fabrication": len([o for o in db if o.status == "Fabricating"])}

@app.post("/api/orders/submit", status_code=status.HTTP_201_CREATED)
def submit_order(order: Order):
    db.append(order)
    return {"order_id": order.order_id, "message": "Order submitted successfully"}

@app.get("/api/orders/{id}/status")
def get_order_status(id: str):
    order = next((o for o in db if o.order_id == id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order.order_id, "status": order.status}
