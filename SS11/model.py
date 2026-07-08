from config import Base
from sqlalchemy import Column, Integer, String, Boolean

class PrakingLot(Base):
    __tablename__ = "parking_slost"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slot_code = Column(String(50), nullable=False, unique=True)
    zone_name = Column(String(50), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=1)
    