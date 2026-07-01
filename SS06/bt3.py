from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI()

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]

class CreateRoom(BaseModel):
    code: str = Field(...)
    name: str = Field(min_length=1, strip_whitespace=True)
    capacity: int = Field(gt=0)
    status: Literal["AVAILABLE", "IN_USE", "MAINTENANCE"]

class CreateRoomBooking(BaseModel):
    room_id: int
    class_name: str = Field(min_length=1, strip_whitespace=True)
    student_count: int = Field(gt=0)
    date: str
    slot: Literal["MORNING", "AFTERNOON", "EVENING"]

@app.get("/rooms", tags=["Rooms"])
def get_rooms(
    keyword: str = Query(default=None),
    status: str = Query(default=None),
    min_capacity: int = Query(default=None)
):
    result = rooms

    if keyword:
        result = [
            room for room in result
            if keyword.lower() in room["code"].lower()
            or keyword.lower() in room["name"].lower()
        ]

    if status:
        result = [
            room for room in result
            if room["status"] == status
        ]

    if min_capacity is not None:
        result = [
            room for room in result
            if room["capacity"] >= min_capacity
        ]

    return result

@app.get("/rooms/{room_id}", tags=["Rooms"])
def get_room_by_id(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return {
                "status": "success",
                "message": "Lấy phòng học thành công",
                "data": room
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )

@app.post("/rooms", status_code=status.HTTP_201_CREATED, tags=["Rooms"])
def create_room(room: CreateRoom):

    for room_item in rooms:
        if room_item["code"] == room.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room code already exists"
            )

    new_room = {
        "id": len(rooms) + 1,
        "code": room.code,
        "name": room.name,
        "capacity": room.capacity,
        "status": room.status
    }

    rooms.append(new_room)

    return {
        "status": "success",
        "message": "Tạo phòng học thành công",
        "data": new_room
    }

@app.put("/rooms/{room_id}", tags=["Rooms"])
def update_room(room_id: int, room: CreateRoom):

    for room_item in rooms:

        if room_item["id"] == room_id:

            for item in rooms:
                if (
                    item["code"] == room.code
                    and item["id"] != room_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Room code already exists"
                    )

            room_item["code"] = room.code
            room_item["name"] = room.name
            room_item["capacity"] = room.capacity
            room_item["status"] = room.status

            return {
                "status": "success",
                "message": "Cập nhật phòng học thành công",
                "data": room_item
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )

@app.delete("/rooms/{room_id}", tags=["Rooms"])
def delete_room(room_id: int):

    for room in rooms:
        if room["id"] == room_id:
            rooms.remove(room)

            return {
                "status": "success",
                "message": "Xóa phòng học thành công"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )

@app.post("/room-bookings", status_code=status.HTTP_201_CREATED, tags=["Room Bookings"])
def create_room_booking(room_booking: CreateRoomBooking):

    room = None

    for room_item in rooms:
        if room_item["id"] == room_booking.room_id:
            room = room_item
            break

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    if room["status"] != "AVAILABLE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not available"
        )

    if room_booking.student_count > room["capacity"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room capacity is not enough"
        )

    for booking in room_bookings:
        if (
            booking["room_id"] == room_booking.room_id
            and booking["date"] == room_booking.date
            and booking["slot"] == room_booking.slot
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room already booked"
            )

    new_booking = {
        "id": len(room_bookings) + 1,
        "room_id": room_booking.room_id,
        "class_name": room_booking.class_name,
        "student_count": room_booking.student_count,
        "date": room_booking.date,
        "slot": room_booking.slot
    }

    room_bookings.append(new_booking)

    return {
        "status": "success",
        "message": "Đặt phòng thành công",
        "data": new_booking
    }


@app.get("/room-bookings", tags=["Room Bookings"])
def get_room_bookings():
    return {
        "status": "success",
        "message": "Lấy danh sách lịch đặt phòng thành công",
        "data": room_bookings
    }