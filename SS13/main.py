from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from pydantic import BaseModel


app = FastAPI()

class MenuItemCreat(BaseModel):
    dish_code : str
    dish_name : str
    calorie_count : int
    price : float

    model_config = 

@app.get("/health", tags=["Health"])
def get_health():
    return{
        "message": "T'm fine."
    }

@app.get("/database", tags=["Database"])
def get_database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Kết nối database thất bại")
    
    else:
        return{
            "message": "kết nối database thành công"
        }

@app.post("/menu-item", tags=["Menu_item"])
def create_menu_item():
