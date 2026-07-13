from database import Base
from sqlalchemy import Column, Integer, String, Float

class Restaurant(Base):
    __tablename__ = "Restaurant"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, nullable=False)


Base.metadata.create_all()
