from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Any, Optional

from b2.database import engine, Base, get_db
from b2.model import BoardingSlot
from b2.schemas import BoardingSlotCreate, BoardingSlotUpdate, BoardingSlotResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Boarding Slots Management API")

def StandardResponse(
    request: Request,
    status_code: int,
    message: str,
    data: Any = None,
    error: Optional[str] = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "error": error,
            "data": data,
            "path": request.url.path,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
    )

@app.post("/boarding-slots", status_code=status.HTTP_201_CREATED)
def create_boarding_slot(request: Request, slot_in: BoardingSlotCreate, db: Session = Depends(get_db)):
    existing_slot = db.query(BoardingSlot).filter(BoardingSlot.slot_number == slot_in.slot_number).first()
    if existing_slot:
        return StandardResponse(
            request=request,
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Slot number already exists",
            error="Bad Request"
        )
    
    db_slot = BoardingSlot(**slot_in.model_dump())
    
    try:
        db.add(db_slot)
        db.commit()
        db.refresh(db_slot)
        
        data_res = BoardingSlotResponse.from_attributes(db_slot).model_dump()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_201_CREATED,
            message="Thêm khoang lưu trú mới thành công",
            data=data_res
        )
    except Exception as e:
        db.rollback()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống khi thêm khoang lưu trú",
            error=str(e)
        )

@app.get("/boarding-slots")
def get_all_boarding_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(BoardingSlot).all()
    data_res = [BoardingSlotResponse.from_attributes(slot).model_dump() for slot in slots]
    
    return StandardResponse(
        request=request,
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách thành công",
        data=data_res
    )

@app.get("/boarding-slots/{slot_id}")
def get_boarding_slot_detail(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not slot:
        return StandardResponse(
            request=request,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Boarding slot not found",
            error="Not Found"
        )
        
    data_res = BoardingSlotResponse.from_attributes(slot).model_dump()
    return StandardResponse(
        request=request,
        status_code=status.HTTP_200_OK,
        message="Lấy chi tiết khoang lưu trú thành công",
        data=data_res
    )

@app.put("/boarding-slots/{slot_id}")
def update_boarding_slot(slot_id: int, request: Request, slot_in: BoardingSlotUpdate, db: Session = Depends(get_db)):
    db_slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not db_slot:
        return StandardResponse(
            request=request,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Boarding slot not found",
            error="Not Found"
        )
    
    if db_slot.slot_number != slot_in.slot_number:
        duplicate_slot = db.query(BoardingSlot).filter(BoardingSlot.slot_number == slot_in.slot_number).first()
        if duplicate_slot:
            return StandardResponse(
                request=request,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Slot number already exists",
                error="Bad Request"
            )

    try:
        update_data = slot_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_slot, key, value)
            
        db.commit()
        db.refresh(db_slot)
        
        data_res = BoardingSlotResponse.from_attributes(db_slot).model_dump()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_200_OK,
            message="Cập nhật thông tin khoang lưu trú thành công",
            data=data_res
        )
    except Exception as e:
        db.rollback()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống khi cập nhật thông tin khoang lưu trú",
            error=str(e)
        )

@app.delete("/boarding-slots/{slot_id}")
def delete_boarding_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    db_slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not db_slot:
        return StandardResponse(
            request=request,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Boarding slot not found",
            error="Not Found"
        )
        
    try:
        db.delete(db_slot)
        db.commit()
        
        return StandardResponse(
            request=request,
            status_code=status.HTTP_200_OK,
            message="Xóa khoang lưu trú thành công",
            data=None
        )
    except Exception as e:
        db.rollback()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống khi xóa khoang lưu trú",
            error=str(e)
        )