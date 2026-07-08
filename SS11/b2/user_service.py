from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator

class SmartHomePlanCreate(BaseModel):
    plan_code: str = Field(..., description="Mã gói thiết bị, bắt buộc, không trùng lặp")
    plan_name: str = Field(..., description="Tên gói thiết bị, bắt buộc")
    device_quantity: int = Field(..., description="Số lượng thiết bị đi kèm")
    price: float = Field(..., description="Đơn giá gói sản phẩm")

    @field_validator("plan_name")
    @classmethod
    def validate_plan_name(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("plan_name không được phép để rỗng.")
        return value.strip()

    @field_validator("device_quantity")
    @classmethod
    def validate_device_quantity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("device_quantity phải là số nguyên lớn hơn 0.")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("price phải là số thực lớn hơn 0.")
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