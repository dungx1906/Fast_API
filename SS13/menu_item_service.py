from sqlalchemy.orm import Session
from model import MenuItem


def create_menu_item_service(db :Session, menu_item_data: dict):
    exists_menu_item = db.query(MenuItem).filter(MenuItem.dish_code==menu_item_data)