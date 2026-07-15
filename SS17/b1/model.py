from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

package_truck = Table(
    "package_truck",
    Base.metadata,
    Column("package_id", Integer, ForeignKey("packages.id"), primary_key=True),
    Column("truck_id", Integer, ForeignKey("trucks.id"), primary_key=True)
)

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)

    packages = relationship("Package", back_populates="warehouse", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Warehouse(id={self.id}, name='{self.warehouse_name}', location='{self.location}')>"

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_code = Column(String(50), unique=True, nullable=False)
    weight = Column(Float, nullable=False)
    
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    warehouse = relationship("Warehouse", back_populates="packages")
    waybill = relationship("Waybill", uselist=False, back_populates="package", cascade="all, delete-orphan")
    trucks = relationship("Truck", secondary=package_truck, back_populates="packages")

    def __repr__(self):
        return f"<Package(id={self.id}, code='{self.package_code}', weight={self.weight})>"

class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tracking_number = Column(String(100), unique=True, nullable=False)
    shipping_status = Column(String(50), nullable=False)
    
    package_id = Column(Integer, ForeignKey("packages.id"), unique=True, nullable=False)

    package = relationship("Package", back_populates="waybill")

    def __repr__(self):
        return f"<Waybill(id={self.id}, tracking='{self.tracking_number}', status='{self.shipping_status}')>"

class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    license_plate = Column(String(20), unique=True, nullable=False)

    packages = relationship("Package", secondary=package_truck, back_populates="trucks")

    def __repr__(self):
        return f"<Truck(id={self.id}, plate='{self.license_plate}')>"