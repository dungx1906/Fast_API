from model import Restaurant
from fastapi import status, HTTPException
from model import Restaurant

def get_all_menu_item():
    if not Restaurant:
        raise ValueError(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy danh sách món ăn"))
    
    return Restaurant

# def get_menu_item_by_category(category: str):
#     category = 