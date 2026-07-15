from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from model import Vehicle

def create_vehicle_service(db: Session, Vehicle_data: dict):
    exists_vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == Vehicle_data["id"])
        .first
    )

    if exists_vehicle:
        return None
    
    new_vehicle = Vehicle(**Vehicle_data)

    db.add(new_vehicle)
    db.flush()

    return new_vehicle


def get_all_vehicle_service(
        db:Session,
        brand:str = None,
        starus:str = None,
        sort_by:str = None,
        order:str = None
):
    query = db.query(Vehicle)

    if brand:
        query = query.filter(
            Vehicle.brand.ilike(f"%{brand}%")
        )

    if starus:
        query = query.filter(
            Vehicle.status == starus
        )

    if sort_by == "daily_rate":
        if order == desc:
            query = query.order_by(desc(Vehicle.daily_rate))
        else:
            query = query.order_by(asc(Vehicle.daily_rate))

    elif sort_by == "production_year":
        if order == desc:
            query = query.order_by(desc(Vehicle.production_year))
        else:
            query = query.order_by(asc(Vehicle.production_year))

    else:
        query = query.order_by(asc(Vehicle.id))

    return query.all()

def get_vehicle_service(db:Session, vehicle_id:str):
    vehicle = (db.query(Vehicle).filter(
        vehicle.id == vehicle_id)
        .first()
    )
    return vehicle

def update_vehicle_service(db:Session, vehicle_id:str, vehicle_data:dict):
    vehicle = (db.query(Vehicle)
               .filter(Vehicle.id == vehicle_id)
               .first
    )
    if vehicle:
        return None
    
    for key, value in vehicle_data.items():
        setattr(vehicle, key, value)

    db.flush

    return vehicle

def delete_vehicle_service(db:Session, vehicle_id:str):
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == vehicle_id)
        .first()
    )
    if not vehicle:
        return False
    
    db.delete(vehicle)
    db.flush
    
    return True

