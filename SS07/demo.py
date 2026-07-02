from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class UserReponse(BaseModel):
    id: int
    username: str
    fullname: str

class BaseUserReponse(BaseModel):
    status: str
    message: str
    data: UserReponse

users = [
    {
        "id": 1,
        "username": "nguyenvana",
        "password": "Abcd@1234",
        "fullname": "Nguyễn Văn A",
        "visa": "012345678"
    },
    {
        "id": 2,
        "username": "tranthib",
        "password": "Tran@123",
        "fullname": "Trần Thị B",
        "visa": "123456789"
    },
    {
        "id": 3,
        "username": "levanc",
        "password": "LeVan@123",
        "fullname": "Lê Văn C",
        "visa": "234567890"
    },
    {
        "id": 4,
        "username": "phamthid",
        "password": "Pham@123",
        "fullname": "Phạm Thị D",
        "visa": "345678901"
    },
    {
        "id": 5,
        "username": "hoange",
        "password": "Hoang@123",
        "fullname": "Hoàng Văn E",
        "visa": "456789012"
    }
]

@app.get("/Users/{User_id}", response_model= BaseUserReponse)
def get_urser_by_id(User_id: int):
    for user in users:
        if user["id"] == User_id:
            return{
                "status": "success",
                "message": "Lấy dữ liệu người dùng thành công",
                "data": user
            }
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")