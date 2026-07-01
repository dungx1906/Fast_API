# Test case 1
# Dữ liệu gửi lên:
# {
#     "student_id": "SV001",
#     "course_id": 1
# }
# Kết quả hiện tại: API vẫn tạo thành công bản ghi đăng ký mới.
# Kết quả đúng mong muốn: API phải trả về lỗi 400 Bad Request với thông báo "Student has already enrolled in this course".
# Lỗi phát hiện: API không kiểm tra học viên đã đăng ký khóa học này hay chưa.

# Test case 2
# Dữ liệu gửi lên:
# {
#     "student_id": "SV002",
#     "course_id": 1
# }
# Kết quả hiện tại: API vẫn cho phép đăng ký thành công mặc dù học viên đã đăng ký khóa học.
# Kết quả đúng mong muốn: API phải trả về lỗi 400 Bad Request với thông báo "Student has already enrolled in this course".
# Lỗi phát hiện: Hệ thống cho phép một học viên đăng ký cùng một khóa học nhiều lần.

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]

class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int

@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate):
    for e in enrollments:
        if e["student_id"] == enrollment.student_id and e["course_id"] == enrollment.course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student has already enrolled in this course"
            )

    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }

    enrollments.append(new_enrollment)

    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }