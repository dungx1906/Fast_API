from database import Base, engine
from sqlalchemy import Column, String, Float, Integer

class Vehicle(Base):
    __tablename__ = "Vehicle"

    id = Column(String(20), primary_key=True, unique=True, nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    daily_rate = Column(Float, nullable=False)
    production_year = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="available")

Base.metadata.create_all(bind=engine)