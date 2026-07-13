from fastapi import FastAPI
from b2.database import engine, Base
from b2.router import student

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    description="Hệ thống API quản lý thông tin sinh viên cho trung tâm đào tạo",
    version="1.0.0"
)

app.include_router(student.router)

@app.get("/")
def root():
    return {"message": "Welcome to Student Management API. Go to /docs to test APIs."}