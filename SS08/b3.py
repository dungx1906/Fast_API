from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


desks = [
    {"id": 1, "desk_number": "DSK-A-01", "zone": "Zone A - Quiet Space", "price_per_day": 150000.0, "status": "AVAILABLE"},
    {"id": 2, "desk_number": "DSK-B-02", "zone": "Zone B - Creative", "price_per_day": 200000.0, "status": "AVAILABLE"},
    {"id": 3, "desk_number": "DSK-C-03", "zone": "Zone C - Panoramic", "price_per_day": 250000.0, "status": "MAINTENANCE"}
]

bookings = [
    {
        "id": 1,
        "desk_id": 1,
        "customer_name": "Nguyen Van A",
        "booking_date": "2026-07-01",
        "payment_status": "PAID"
    }
]


class Desk(BaseModel):
    desk_number: str
    zone: str
    price_per_day: float = Field(gt=0)
    status: str


class Booking(BaseModel):
    desk_id: int
    customer_name: str
    booking_date: str
    payment_status: str


@app.post("/desks", status_code=201)
def create_desk(desk: Desk):

    for d in desks:
        if d["desk_number"] == desk.desk_number:
            raise HTTPException(status_code=400, detail="Desk number already exists")

    if desk.status not in ["AVAILABLE", "UNAVAILABLE", "MAINTENANCE"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    new_desk = {
        "id": max([d["id"] for d in desks], default=0) + 1,
        "desk_number": desk.desk_number,
        "zone": desk.zone,
        "price_per_day": desk.price_per_day,
        "status": desk.status
    }

    desks.append(new_desk)

    return new_desk


@app.get("/desks")
def get_desks(zone_keyword: str = "", max_price: float = 0, status: str = ""):

    result = desks

    if zone_keyword != "":
        result = [
            d for d in result
            if zone_keyword.lower() in d["zone"].lower()
        ]

    if max_price > 0:
        result = [
            d for d in result
            if d["price_per_day"] <= max_price
        ]

    if status != "":
        result = [
            d for d in result
            if d["status"] == status
        ]

    return result


@app.get("/desks/{desk_id}")
def get_desk(desk_id: int):

    for desk in desks:
        if desk["id"] == desk_id:
            return desk

    raise HTTPException(status_code=404, detail="Desk not found")


@app.put("/desks/{desk_id}")
def update_desk(desk_id: int, desk: Desk):

    for d in desks:

        if d["id"] != desk_id and d["desk_number"] == desk.desk_number:
            raise HTTPException(status_code=400, detail="Desk number already exists")

    if desk.status not in ["AVAILABLE", "UNAVAILABLE", "MAINTENANCE"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    for d in desks:
        if d["id"] == desk_id:
            d["desk_number"] = desk.desk_number
            d["zone"] = desk.zone
            d["price_per_day"] = desk.price_per_day
            d["status"] = desk.status
            return d

    raise HTTPException(status_code=404, detail="Desk not found")


@app.delete("/desks/{desk_id}", status_code=204)
def delete_desk(desk_id: int):

    for desk in desks:
        if desk["id"] == desk_id:
            desks.remove(desk)
            return

    raise HTTPException(status_code=404, detail="Desk not found")


@app.post("/bookings", status_code=201)
def create_booking(booking: Booking):

    desk = None

    for d in desks:
        if d["id"] == booking.desk_id:
            desk = d
            break

    if desk is None:
        raise HTTPException(status_code=404, detail="Desk not found")

    if desk["status"] != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Desk is not available")

    if booking.payment_status not in ["PENDING", "PAID", "CANCELLED"]:
        raise HTTPException(status_code=400, detail="Invalid payment status")

    for b in bookings:
        if (
            b["desk_id"] == booking.desk_id
            and b["booking_date"] == booking.booking_date
        ):
            raise HTTPException(
                status_code=400,
                detail="Desk already booked on this date"
            )

    new_booking = {
        "id": max([b["id"] for b in bookings], default=0) + 1,
        "desk_id": booking.desk_id,
        "customer_name": booking.customer_name,
        "booking_date": booking.booking_date,
        "payment_status": booking.payment_status
    }

    bookings.append(new_booking)

    return new_booking


@app.get("/bookings")
def get_bookings():
    return bookings