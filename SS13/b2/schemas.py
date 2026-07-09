from pydantic import BaseModel, Field, field_validator
from typing import Literal

class BoardingSlotBase(BaseModel):
    slot_number: str = Field(..., max_length=50)
    room_size: Literal["SMALL", "MEDIUM", "LARGE"]
    price_per_day: float = Field(..., gt=0.0)
    status: Literal["VACANT", "OCCUPIED"] = "VACANT"

    @field_validator('slot_number')
    @classmethod
    def slot_number_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('slot_number không được để rỗng hoặc chỉ chứa khoảng trắng')
        return v.strip()

class BoardingSlotCreate(BoardingSlotBase):
    pass

class BoardingSlotUpdate(BoardingSlotBase):
    pass

class BoardingSlotResponse(BaseModel):
    id: int
    slot_number: str
    room_size: str
    price_per_day: float
    status: str

    class Config:
        from_attributes = True