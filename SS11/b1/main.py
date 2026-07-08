from fastapi import FastAPI, status, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from b1.database import engine, Base, get_db
from b1.model import ParkingSlotModel
from b1.user_service import ParkingSlotCreate, StandardResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/parking_slots", status_code=status.HTTP_201_CREATED)
def create_parking_slot(requets: Request, slot_data: ParkingSlotCreate, db: Session= Depends(get_db)):
    db_slot = ParkingSlotModel(
        slot_code = slot_data.slot_code,
        zone_name = slot_data.zone_name,
        max_weight = slot_data.max_weight,
        is_available= slot_data.is_available if slot_data.is_available is not None else True
    )
    try:
        db.add(db_slot)
        db.commit()
        db.refresh(db_slot)
    except IntegrityError:
        db.rollback()
        return StandardResponse(
            statusCode=status.HTTP_400_BAD_REQUEST,
            message=f"Slot code {slot_data.slot_code} đã tồn tại.",
            error="Bad Request",
            data=None,
            path=requets.url.path
        )
        
    except Exception as e:
        db.rollback()
        return StandardResponse(
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống khi lưu trữ dữ liệu",
            error=str(e),
            data=None,
            path=requets.url.path
        )
    slot_respone_data = {
        "id": db_slot.id,
        "slot_code": db_slot.slot_code,
        "zone_name": db_slot.zone_name,
        "max_weight": db_slot.max_weight,
        "is_available": db_slot.is_available
    }
    return StandardResponse(
        statusCode=201,
        message="Thêm vị trí đỗ xe thành công",
        error=None,
        data=slot_respone_data,
        path=requets.url.path   
    )
    
@app.get("/parking_slots")
def get__all_parkng_slots(requets: Request, db: Session = Depends(get_db)):
    slots = db.query(ParkingSlotModel).all()
    
    list_data = [
        {
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        }
        for slot in slots
    ]
    
    return StandardResponse(
        statusCode=200,
        message="Lấy danh sách vị trí đỗ xe thành công",
        error=None,
        data=list_data,
        path=requets.url.path
    )

@app.get("/parking_slots/{slot_id}")
def get_parking_slot_detail(
    slot_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    slot = db.query(ParkingSlotModel).filter(ParkingSlotModel.id == slot_id).first()
    
    if slot is None:
        return StandardResponse(
            statusCode=404,
            message="Parking slot not found",
            error="Not Found",
            data=None,
            path=request.url.path
        )
        
    slot_response_data = {
        "id": slot.id,
        "slot_code": slot.slot_code,
        "zone_name": slot.zone_name,
        "max_weight": slot.max_weight,
        "is_available": slot.is_available
    }
    return StandardResponse(
        statusCode=200,
        message="Lấy thông tin chi tiết vị trí đỗ xe thành công",
        error=None,
        data=slot_response_data,
        path=request.url.path
    )
