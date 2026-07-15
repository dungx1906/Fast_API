import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/center_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), default="ACTIVE")

    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(20), default="OPEN")

    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

Base.metadata.create_all(bind=engine)

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime.datetime

    class Config:
        from_attributes = True

class CourseShortResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class StudentCoursesResponse(BaseModel):
    student_id: int
    full_name: str
    courses: list[CourseShortResponse]

app = FastAPI()

@app.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại.")

    course = db.query(Course).filter(Course.id == payload.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại.")

    if student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Sinh viên đã ngừng học (INACTIVE).")

    if course.status != "OPEN":
        raise HTTPException(status_code=400, detail="Khóa học hiện đang đóng (CLOSED).")

    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == payload.student_id,
        Enrollment.course_id == payload.course_id
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Sinh viên đã đăng ký khóa học này từ trước.")

    current_students_count = db.query(func.count(Enrollment.id)).filter(
        Enrollment.course_id == payload.course_id
    ).scalar()
    
    if current_students_count >= course.max_students:
        raise HTTPException(status_code=400, detail="Khóa học đã đủ số lượng học viên tối đa.")

    new_enrollment = Enrollment(
        student_id=payload.student_id,
        course_id=payload.course_id,
        enrolled_at=datetime.datetime.now()
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    
    return new_enrollment

@app.get("/students/{student_id}/courses", response_model=StudentCoursesResponse)
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại.")

    registered_courses = [enrollment.course for enrollment in student.enrollments]

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": registered_courses
    }