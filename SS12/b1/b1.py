from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/ecommerce_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

class ProductUpdate(BaseModel):
    name: str
    price: float

app = FastAPI()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@app.put("/products/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    # db = SessionLocal()
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()
    

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product not found"
        )

    product.name = product_update.name
    product.price = product_update.price
    
    db.commit()
    db.refresh(product)

    return {
        "message": "Product updated successfully",
        "data": {
            "id": product.id,
            "name": product.name,
            "price": float(product.price)
        }
    }