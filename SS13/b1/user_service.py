from pydantic import BaseModel, Field, field_validator
from typing import Literal

class MenuItemBase(BaseModel):
    dish_code: str = Field(..., max_length=50)
    dish_name: str = Field(..., min_length=1, max_length=100)
    calorie_count: int = Field(..., gt=0)
    price: float = Field(..., gt=0.0)
    status: Literal["AVAILABLE", "OUT_OF_STOCK"] = "AVAILABLE"

    @field_validator('dish_name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('dish_name không được để rỗng hoặc chỉ chứa khoảng trắng')
        return v.strip()

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    pass

class MenuItemResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    class Config:
        from_attributes = True