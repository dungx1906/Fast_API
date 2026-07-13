from sqlalchemy.orm import Session
from b2.model.student import Student
from b2.schemas.student import StudentCreate

def get_all_students(db: Session):
    return db.query(Student).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def create_student(db: Session, student_data: StudentCreate):
    db_student = Student(
        full_name=student_data.full_name,
        email=student_data.email,
        major=student_data.major,
        gpa=student_data.gpa
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student_data: StudentCreate):
    db_student = get_student_by_id(db, student_id)
    if not db_student:  # Nếu không tìm thấy trả về None để router xử lý 404
        return None
    
    db_student.full_name = student_data.full_name
    db_student.email = student_data.email
    db_student.major = student_data.major
    db_student.gpa = student_data.gpa
    
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None
    db.delete(db_student)
    db.commit()
    return db_student