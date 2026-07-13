from pydantic import BaseModel, EmailStr

class StudentBase(BaseModel):
    full_name: str
    email: EmailStr  
    major: str
    gpa: float

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True 