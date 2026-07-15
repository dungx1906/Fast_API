import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship


DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/workshop_db"

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
    student_code = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    status = Column(String(20), default="ACTIVE") 

    registrations = relationship("Registration", back_populates="student")

class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(255))
    maximum_participants = Column(Integer, nullable=False)
    status = Column(String(20), default="UPCOMING")  
    start_time = Column(DateTime, nullable=False)


    registrations = relationship("Registration", back_populates="workshop")

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.datetime.now)
    status = Column(String(20), default="CONFIRMED")  # CONFIRMED, CANCELLED

    student = relationship("Student", back_populates="registrations")
    workshop = relationship("Workshop", back_populates="registrations")

Base.metadata.create_all(bind=engine)

class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    email: EmailStr

class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: str
    status: str
    class Config:
        from_attributes = True

class WorkshopCreate(BaseModel):
    title: str
    description: Optional[str] = None
    maximum_participants: int
    start_time: datetime.datetime

class WorkshopResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    maximum_participants: int
    status: str
    start_time: datetime.datetime
    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    student_id: int
    workshop_id: int

class RegistrationResponse(BaseModel):
    id: int
    student_id: int
    workshop_id: int
    registered_at: datetime.datetime
    status: str
    class Config:
        from_attributes = True

class StudentShort(BaseModel):
    id: int
    student_code: str
    full_name: str
    class Config:
        from_attributes = True

class WorkshopShort(BaseModel):
    id: int
    title: str
    start_time: datetime.datetime
    class Config:
        from_attributes = True

class WorkshopWithStudentsResponse(BaseModel):
    workshop_id: int
    title: str
    students: List[StudentShort]

class StudentWithWorkshopsResponse(BaseModel):
    student_id: int
    full_name: str
    workshops: List[WorkshopShort]


app = FastAPI(title="Hệ thống Quản lý Đăng ký Workshop")

@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(
        (Student.student_code == payload.student_code) | (Student.email == payload.email)
    ).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Mã sinh viên hoặc Email đã được đăng ký trên hệ thống.")
    
    new_student = Student(**payload.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/students", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.post("/workshops", response_model=WorkshopResponse, status_code=status.HTTP_201_CREATED)
def create_workshop(payload: WorkshopCreate, db: Session = Depends(get_db)):
    if payload.maximum_participants <= 0:
        raise HTTPException(status_code=400, detail="Số lượng thành viên tối đa phải lớn hơn 0.")
    
    new_workshop = Workshop(**payload.model_dump())
    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)
    return new_workshop

@app.get("/workshops", response_model=List[WorkshopResponse])
def get_all_workshops(db: Session = Depends(get_db)):
    return db.query(Workshop).all()

@app.get("/workshops/{id}", response_model=WorkshopResponse)
def get_workshop_detail(id: int, db: Session = Depends(get_db)):
    workshop = db.query(Workshop).filter(Workshop.id == id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Không tìm thấy workshop yêu cầu.")
    return workshop

@app.post("/registrations", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_workshop(payload: RegistrationCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại.")
    if student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Tài khoản sinh viên này đã bị khóa hoặc ngừng hoạt động.")

    workshop = db.query(Workshop).filter(Workshop.id == payload.workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop không tồn tại.")

    if workshop.status != "UPCOMING":
        raise HTTPException(status_code=400, detail=f"Không thể đăng ký. Workshop hiện đang ở trạng thái: {workshop.status}")

    existing_reg = db.query(Registration).filter(
        Registration.student_id == payload.student_id,
        Registration.workshop_id == payload.workshop_id,
        Registration.status == "CONFIRMED"
    ).first()
    if existing_reg:
        raise HTTPException(status_code=400, detail="Sinh viên này đã đăng ký tham gia workshop này từ trước.")

    active_slots = db.query(func.count(Registration.id)).filter(
        Registration.workshop_id == payload.workshop_id,
        Registration.status == "CONFIRMED"
    ).scalar()
    if active_slots >= workshop.maximum_participants:
        raise HTTPException(status_code=400, detail="Thành viên đã đủ. Workshop đã đạt số lượng giới hạn tối đa.")

    new_registration = Registration(
        student_id=payload.student_id,
        workshop_id=payload.workshop_id,
        status="CONFIRMED"
    )
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return new_registration

@app.get("/students/{id}/workshops", response_model=WorkshopWithStudentsResponse)
def get_workshops_by_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại.")
    
    workshops = [reg.workshop for reg in student.registrations if reg.status == "CONFIRMED"]
    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "workshops": workshops
    }

@app.get("/workshops/{id}/students", response_model=WorkshopWithStudentsResponse)
def get_students_by_workshop(id: int, db: Session = Depends(get_db)):
    workshop = db.query(Workshop).filter(Workshop.id == id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop không tồn tại.")
        

    students = [reg.student for reg in workshop.registrations if reg.status == "CONFIRMED"]
    return {
        "workshop_id": workshop.id,
        "title": workshop.title,
        "students": students
    }

@app.put("/registrations/{id}/cancel", response_model=RegistrationResponse)
def cancel_registration(id: int, db: Session = Depends(get_db)):
    registration = db.query(Registration).filter(Registration.id == id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Không tìm thấy bản ghi đăng ký yêu cầu.")
    
    if registration.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Bản ghi đăng ký này đã được hủy trước đó.")
        
    registration.status = "CANCELLED"
    db.commit()
    db.refresh(registration)
    return registration