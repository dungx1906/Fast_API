from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any

class ParkingLotCreate(BaseModel):
    slot_code: str = Field(..., max_length=50)
    zone_name: str = Field(..., min_length=3, max_length=255)
    max_weight: int = Field(..., gt=0)

    @field_validator("zone_name")
    def not_empty(cls, v:str):
        if not v.strip():
            raise Exception("zone name not empty")
        return v.strip()
    
class ParkingLotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    slot_code: str
    zone_name: str
    max_weight: int
    is_available: bool
class ApiResponse(BaseModel):
    statusCode: int
    message: str
    error: str
    data: Optional[str] = None
    path: Optional[Any] = None
    timestamp: str