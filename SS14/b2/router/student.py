from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from b2.database import get_db
from b2.schemas.student import StudentCreate, StudentResponse
from b2.services import student as student_service

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.get("/", response_model=List[StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = student_service.get_student_by_id(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, student)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    updated_student = student_service.update_student(db, student_id, student)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted_student = student_service.delete_student(db, student_id)
    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return None