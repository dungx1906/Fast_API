from sqlalchemy import Column, Integer, String, Float
from b2.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    major = Column(String(255), nullable=False)
    gpa = Column(Float, nullable=False)