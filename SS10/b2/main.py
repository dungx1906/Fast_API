from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ecommerce_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    total_price = Column(Integer)

app = FastAPI()

@app.get("/orders/{order_id}")
def get_order_detail(order_id: int):
    db = SessionLocal()
    try:
        order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Order not found", "code": "ORDER_NOT_EXIST"}
            )
            
        return {"id": order.id, "customer": order.customer_name}
        
    finally:
        db.close() 