from database import Base, engine
from sqlalchemy import Column, Integer, String, Float


class MenuItem(Base):
    __tablename__ = "menu_item"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dish_code = Column(String(50), unique=True, nullable=False, index=True)
    dish_name = Column(String(255), nullable=False)
    calorie_count = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(30), default="AVAILABLE", nullable=False)

    Base.metadata.create_all(engine)


