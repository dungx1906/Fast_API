from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders = []

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    order_id: int
    product_id: int
    product_name: str
    quantity: int
    total_price: float

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    product = next((p for p in products if p["id"] == order.product_id), None)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Sản phẩm không tồn tại")

    if order.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Số lượng mua phải lớn hơn 0")

    if order.quantity > product["stock"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Sản phẩm không đủ số lượng trong kho")

    product["stock"] -= order.quantity

    new_order = {
        "order_id": len(orders) + 1,
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": order.quantity,
        "total_price": product["price"] * order.quantity
    }
    orders.append(new_order)

    return new_order