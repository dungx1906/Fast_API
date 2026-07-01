from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel, Field

class CreateCourse(BaseModel):
    code: str = Field(...)
    name: str = Field(min_length=1, strip_whitespace=True)
    duration: int = Field(gt=1)
    fee: int = Field(gt=0)

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

@app.get("/courses", tags=["Courses"])
def get_courses(
    keyword: str = Query(default=None),
    min_fee: int = Query(default=None),
    max_fee: int = Query(default=None)
):
    result = courses

    if keyword:
        result = [
            course for course in result
            if keyword.lower() in course["name"].lower()
            or keyword.lower() in course["code"].lower()
        ]

    if min_fee is not None:
        result = [
            course for course in result
            if course["fee"] >= min_fee
        ]

    if max_fee is not None:
        result = [
            course for course in result
            if course["fee"] <= max_fee
        ]

    return result

@app.get("/courses/{course_id}", tags=["Courses"])
def get_course_by_id(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return {
                "status": "success",
                "message": "Lấy khóa học thành công",
                "data": course
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Không tìm thấy khóa học"
    )

@app.post("/courses", status_code=status.HTTP_201_CREATED, tags=["Courses"])
def create_course(course: CreateCourse):

    for item in courses:
        if item["code"] == course.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Đã có mã khóa học rồi"
            )

    new_course = {
        "id": len(courses) + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    courses.append(new_course)

    return {
        "status": "success",
        "message": "Tạo mới khóa học thành công",
        "data": new_course
    }

@app.put("/courses/{course_id}", tags=["Courses"])
def update_course(course_id: int, course: CreateCourse):

    for item in courses:
        if item["id"] == course_id:

            for course_item in courses:
                if (
                    course_item["code"] == course.code
                    and course_item["id"] != course_id
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Đã có mã khóa học rồi"
                    )

            item["code"] = course.code
            item["name"] = course.name
            item["duration"] = course.duration
            item["fee"] = course.fee

            return {
                "status": "success",
                "message": "Cập nhật khóa học thành công",
                "data": item
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Không tìm thấy khóa học"
    )

@app.delete("/courses/{course_id}", tags=["Courses"])
def delete_course(course_id: int):

    for item in courses:
        if item["id"] == course_id:
            courses.remove(item)

            return {
                "status": "success",
                "message": "Xóa khóa học thành công"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Không tìm thấy khóa học"
    )