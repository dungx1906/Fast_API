from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr

class CreateStudent(BaseModel):
    code: str = Field(...)
    name: str = Field(min_length=1, strip_whitespace=True)
    email: EmailStr
    age: int = Field(ge=18)

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


# Lấy danh sách học viên + tìm kiếm + lọc
@app.get("/students", tags=["Students"])
def get_students(
    keyword: str = Query(default=None),
    min_age: int = Query(default=None),
    max_age: int = Query(default=None)
):
    result = students

    if keyword:
        result = [
            student for student in result
            if keyword.lower() in student["name"].lower()
            or keyword.lower() in student["code"].lower()
            or keyword.lower() in student["email"].lower()
        ]

    if min_age is not None:
        result = [
            student for student in result
            if student["age"] >= min_age
        ]

    if max_age is not None:
        result = [
            student for student in result
            if student["age"] <= max_age
        ]

    return result


# Lấy chi tiết học viên
@app.get("/students/{student_id}", tags=["Students"])
def get_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {
                "status": "success",
                "message": "Lấy học viên thành công",
                "data": student
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Không tìm thấy học viên"
    )


# Thêm học viên
@app.post("/students", status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: CreateStudent):

    for item in students:
        if item["code"] == student.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Đã có mã học viên rồi"
            )

        if item["email"] == student.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã tồn tại"
            )

    new_student = {
        "id": len(students) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "status": "success",
        "message": "Tạo mới học viên thành công",
        "data": new_student
    }


# Cập nhật học viên
@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, student: CreateStudent):

    for item in students:
        if item["id"] == student_id:

            for student_item in students:
                if (
                    student_item["code"] == student.code
                    and student_item["id"] != student_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Đã có mã học viên rồi"
                    )

                if (
                    student_item["email"] == student.email
                    and student_item["id"] != student_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email đã tồn tại"
                    )

            item["code"] = student.code
            item["name"] = student.name
            item["email"] = student.email
            item["age"] = student.age

            return {
                "status": "success",
                "message": "Cập nhật học viên thành công",
                "data": item
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Không tìm thấy học viên"
    )


# Xóa học viên
@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int):

    for item in students:
        if item["id"] == student_id:
            students.remove(item)

            return {
                "status": "success",
                "message": "Xóa học viên thành công"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Không tìm thấy học viên"
    )