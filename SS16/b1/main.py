from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    class_id: int

classrooms = [
    {
        "id": 1,
        "name": "FastAPI Basic",
        "max_students": 2,
        "status": "OPEN"
    },
    {
        "id": 2,
        "name": "Python Foundation",
        "max_students": 3,
        "status": "CLOSED"
    }
]

students = [
    {
        "id": 1,
        "student_code": "SV001",
        "full_name": "Nguyễn Văn An",
        "class_id": 1
    },
    {
        "id": 2,
        "student_code": "SV002",
        "full_name": "Trần Minh Bình",
        "class_id": 1
    }
]

@app.get("/classrooms")
def get_classrooms():
    return classrooms

@app.get("/students")
def get_students():
    return students

@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED
)
def create_student(student_data: StudentCreate):
    duplicated_student = next(
        (
            student
            for student in students
            if student["student_code"] == student_data.student_code
        ),
        None
    )

    if duplicated_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mã sinh viên đã tồn tại trong hệ thống"
        )

    classroom = next(
        (
            classroom
            for classroom in classrooms
            if classroom["id"] == student_data.class_id
        ),
        None
    )

    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_44_NOT_FOUND,
            detail="Lớp học không tồn tại"
        )

    if classroom["status"] != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học đang không ở trạng thái OPEN"
        )

    current_students = [
        student
        for student in students
        if student["class_id"] == student_data.class_id
    ]

    if len(current_students) >= classroom["max_students"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học đã đủ số lượng tối đa"
        )

    new_student = {
        "id": len(students) + 1,
        "student_code": student_data.student_code,
        "full_name": student_data.full_name,
        "class_id": student_data.class_id
    }

    students.append(new_student)
    return new_student