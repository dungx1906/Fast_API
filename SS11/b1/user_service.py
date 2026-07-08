from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator

class ParkingSlotCreate(BaseModel):
    slot_code: str = Field(..., description="Mã vị trí đỗ, không trùng lặp")
    zone_name: str = Field(..., description="Tên khu vực")
    max_weight: int = Field(..., description="Tải trọng tối đa (kg)")
    is_available: Optional[bool] = True

    @field_validator("zone_name")
    @classmethod
    def validate_zone_name(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise ValueError("zone_name không được rỗng và có độ dài tối thiểu là 3 ký tự")
        return cleaned

    @field_validator("max_weight")
    @classmethod
    def validate_max_weight(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("max_weight phải là số nguyên lớn hơn 0")
        return value

def StandardResponse(
    statusCode: int,
    message: str,
    error: Optional[str],
    data: Any,
    path: str
):
    timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "statusCode": statusCode,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": timestamp_str
    }