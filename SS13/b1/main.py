from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Any, Optional

from b1.database import engine, Base, get_db
from b1.model import MenuItem
from b1.user_service import MenuItemCreate, MenuItemUpdate, MenuItemResponse

# Khởi tạo các bảng trong database (nếu chưa có)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Menu Items Management API")

# --- Helper Function để chuẩn hóa cấu trúc Response ---
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

# --- 1. POST: Thêm món ăn mới ---
@app.post("/menu-items", status_code=status.HTTP_201_CREATED)
def create_menu_item(request: Request, item_in: MenuItemCreate, db: Session = Depends(get_db)):
    # Kiểm tra trùng lặp dish_code
    existing_item = db.query(MenuItem).filter(MenuItem.dish_code == item_in.dish_code).first()
    if existing_item:
        return StandardResponse(
            request=request,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Dish code '{item_in.dish_code}' đã tồn tại trong hệ thống.",
            error="Bad Request"
        )
    
    db_item = MenuItem(**item_in.model_dump())
    
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        

        data_res = MenuItemResponse.from_attributes(db_item).model_dump()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_201_CREATED,
            message="Thêm món ăn mới thành công",
            data=data_res
        )
    except Exception as e:
        db.rollback()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống khi thêm món ăn",
            error=str(e)
        )

@app.get("/menu-items")
def get_all_menu_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(MenuItem).all()
    data_res = [MenuItemResponse.from_attributes(item).model_dump() for item in items]
    
    return StandardResponse(
        request=request,
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách món ăn thành công",
        data=data_res
    )

@app.get("/menu-items/{item_id}")
def get_menu_item_detail(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        return StandardResponse(
            request=request,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Menu item not found",
            error="Not Found"
        )
        
    data_res = MenuItemResponse.from_attributes(item).model_dump()
    return StandardResponse(
        request=request,
        status_code=status.HTTP_200_OK,
        message="Lấy thông tin chi tiết món ăn thành công",
        data=data_res
    )
@app.put("/menu-items/{item_id}")
def update_menu_item(item_id: int, request: Request, item_in: MenuItemUpdate, db: Session = Depends(get_db)):
    # Tìm món ăn hiện tại bằng ID
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        return StandardResponse(
            request=request,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Menu item not found",
            error="Not Found"
        )
    
    if db_item.dish_code != item_in.dish_code:
        duplicate_code = db.query(MenuItem).filter(MenuItem.dish_code == item_in.dish_code).first()
        if duplicate_code:
            return StandardResponse(
                request=request,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"Dish code '{item_in.dish_code}' đã được sử dụng bởi món ăn khác.",
                error="Bad Request"
            )

    try:
        update_data = item_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
            
        db.commit()
        db.refresh(db_item)
        
        data_res = MenuItemResponse.from_attributes(db_item).model_dump()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_200_OK,
            message="Cập nhật món ăn thành công",
            data=data_res
        )
    except Exception as e:
        db.rollback()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống khi cập nhật món ăn",
            error=str(e)
        )

@app.delete("/menu-items/{item_id}")
def delete_menu_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        return StandardResponse(
            request=request,
            status_code=status.HTTP_404_NOT_FOUND,
            message="Menu item not found",
            error="Not Found"
        )
        
    try:
        db.delete(db_item)
        db.commit()
        
        return StandardResponse(
            request=request,
            status_code=status.HTTP_200_OK,
            message="Xóa món ăn thành công",
            data=None
        )
    except Exception as e:
        db.rollback()
        return StandardResponse(
            request=request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống khi xóa món ăn",
            error=str(e)
        )