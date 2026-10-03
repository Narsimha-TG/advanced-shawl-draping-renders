from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import uuid

app = FastAPI(title="Luxury Hotel Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data store
hotels = [
    {"id": "1", "property_name": "The Grand Azure", "room_type": "Suite", "price_per_night": 1200, "availability_status": True},
    {"id": "2", "property_name": "Midnight Palms", "room_type": "Villa", "price_per_night": 2500, "availability_status": True}
]

reservations = {}

class Reservation(BaseModel):
    property_id: str
    check_in_date: date
    check_out_date: date
    guest_details: dict

@app.get("/api/v1/hotels")
def get_hotels():
    return hotels

@app.get("/api/v1/hotels/{id}")
def get_hotel(id: str):
    hotel = next((h for h in hotels if h["id"] == id), None)
    if not hotel:
        raise HTTPException(status_code=404, detail="Property not found")
    return hotel

@app.post("/api/v1/reservations", status_code=status.HTTP_201_CREATED)
def create_reservation(res: Reservation):
    res_id = str(uuid.uuid4())
    reservations[res_id] = {**res.dict(), "id": res_id, "payment_status": "pending"}
    return {"id": res_id, "status": "created"}

@app.get("/api/v1/reservations/{id}")
def get_reservation(id: str):
    if id not in reservations:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservations[id]

@app.post("/api/v1/payments/process")
def process_payment(payment_data: dict):
    # Mock payment gateway logic
    return {"status": "success", "transaction_id": str(uuid.uuid4())}