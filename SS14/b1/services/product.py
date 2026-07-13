from sqlalchemy.orm import Session
from b1.model.product import Product
from b1.schemas.product import ProductCreate

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product_data: ProductCreate):
    db_product = Product(name=product_data.name, price=product_data.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_data: ProductCreate):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    db_product.name = product_data.name
    db_product.price = product_data.price
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    return db_product