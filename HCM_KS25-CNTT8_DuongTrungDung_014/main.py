from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI()

@app.get("/heath")
def heath(db:Session, Depends(get_db)):
    try:


    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Không kết nối được data")
    
    else:
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="API đang chạy"
        )
    