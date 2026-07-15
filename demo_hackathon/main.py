from fastapi import FastAPI, HTTPException, status, Depends, Request
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
import menu_item_service

app = FastAPI()

class VehicleCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:str = Field(
        min_length=1,
        max_length=20,
        description="Vehicle id"
    )

    brand:str = Field(
        min_length=2,
        max_length=20
    )

    model: str = Field(
        min_length=1,
        max_length=50
    )

    daily_rate:float = Field(gt=0)

    production_year: int = Field(
        ge=2010,
        le=2026
    )

    status:str = Field(default="available")

    @field_validator("brand")
    @classmethod
    def validate_brand(cls, value:str):
        value = value.strip()

        if not value:
            raise ValueError ("Brand không được để trống")
        
        return value
        
    @field_validator("model")
    @classmethod
    def validate_model(cls, value:str):
        value = value.strip()

        if not value:
            raise ValueError("model không được để trống")
        
        return value
    
    @field_validator("production_year")
    @classmethod
    def validate_production_year(cls, value):
        if not (value >= 2010 and value <=2026):
            raise ValueError("production year phải nằm trong khoảng năm (2010-2026)")
        
        return value
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str):
        value = value.lower()

        allow_status = [
            "available",
            "rented",
            "maintenance"
        ]

        if value not in allow_status:
            raise ValueError ("status phải là available, rented, maintenance")
        
        return value
    
class UpdateVehicle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    brand: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    model: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    daily_rate: Optional[float] = Field(
        default=None,
        gt=0
    )

    production_year: Optional[int] = Field(
        default=None,
        ge=2010,
        le=2026
    )

    status: Optional[str] = Field(
        default="available"
    )

def create_response(
    status_code:int,
    message:str,
    path:str,
    data = None,
    error = None
):

    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode":status_code,
            "data":data,
            "message":message,
            "timestamp":datetime.now().isoformat(),
            "path":path,
            "error":error
        }
    )

@app.get("/vehicle", tags=["Vehicle"])
def get_all_vehicle(
    request :Request,
    brand:Optional[str] = None,
    vehicle_status: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: str = "asc",
    db:Session = Depends(get_db)
):
    try:
        vehicles = menu_item_service.get_all_vehicle_service(
            db=db,
            brand=brand,
            status=vehicle_status,
            sort_by=sort_by,
            order=order
        )

    except Exception as e:
        print(e)
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không lấy được xe"
        )
    
    else:
        return create_response(
            status_code=status.HTTP_200_OK,
            message="lấy dữ liệu thành công",
            data=[
                VehicleCreate.model_validate(vehicle).model_dump()
                for vehicle in vehicles
            ],
            path=request.url.path

        )



@app.get("/vehicle/{vehicle_id}", tags=["Vehicle"])
def get_vehicle_by_id(
    vehicle_id:str,
    request : Request,
    db:Session = Depends(get_db)
):
    try:
        vehicle = menu_item_service.get_vehicle_service(db, vehicle_id)
    
    except Exception as e:
        print(e)
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không lấy được xe"
        )
    
    else:
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="không tìm thấy xe"
            )
        
        return create_response(
            status_code=status.HTTP_200_OK,
            message="lấy dữ liệu thành công",
            data=VehicleCreate.model_validate(vehicle).model_dump(),
            path=request.url.path
        )
    

@app.post("/vehicles", tags=["Vehicle"])
def create_vehicle(
    request_body: VehicleCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        new_vehicle = menu_item_service.create_vehicle_service(
            db,
            request_body.model_dump()
        )

    except Exception as e:
        print(e)
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create vehicle."
        )

    else:

        if new_vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vehicle ID already exists."
            )

        db.commit()
        db.refresh(new_vehicle)

        return create_response(
            status_code=status.HTTP_201_CREATED,
            message="Vehicle created successfully.",
            data=VehicleCreate.model_validate(new_vehicle).model_dump(),
            path=request.url.path
        )

@app.put("/vehicles/{vehicle_id}", tags=["Vehicle"])
def update_vehicle(
    vehicle_id: str,
    request_body: UpdateVehicle,
    request: Request,
    db: Session = Depends(get_db)
):
    try:

        vehicle = menu_item_service.update_vehicle_service(
            db,
            vehicle_id,
            request_body.model_dump(exclude_unset=True)
        )

    except Exception as e:
        print(e)
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update vehicle."
        )

    else:

        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found."
            )

        db.commit()
        db.refresh(vehicle)

        return create_response(
            status_code=status.HTTP_200_OK,
            message="Vehicle updated successfully.",
            data=VehicleCreate.model_validate(vehicle).model_dump(),
            path=request.url.path
        )

@app.delete("/vehicles/{vehicle_id}", tags=["Vehicle"])
def delete_vehicle(
    vehicle_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    try:

        is_deleted = menu_item_service.delete_vehicle_service(
            db,
            vehicle_id
        )

    except Exception as e:
        print(e)
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete vehicle."
        )

    else:

        if not is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found."
            )

        db.commit()

        return create_response(
            status_code=status.HTTP_200_OK,
            message="Vehicle deleted successfully.",
            data=None,
            path=request.url.path
        )