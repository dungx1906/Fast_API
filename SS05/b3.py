from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int

@app.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(registration: RegistrationCreate):

    if not any(student["id"] == registration.student_id for student in students):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    course = None
    for item in courses:
        if item["id"] == registration.course_id:
            course = item
            break

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    for registration_item in registrations:
        if (
            registration_item["student_id"] == registration.student_id
            and registration_item["course_id"] == registration.course_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already registered this course"
            )

    total_registration = 0
    for registration_item in registrations:
        if registration_item["course_id"] == registration.course_id:
            total_registration += 1

    if total_registration >= course["capacity"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is full"
        )

    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }

    registrations.append(new_registration)

    return {
        "message": "Registration created successfully",
        "data": new_registration
    }