from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field

class ProductCreated(BaseModel):
    name: str = Field(min_length=1, strip_whitespace=True)
    price: float = Field(gt=0) 

app = FastAPI()

products = [

    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]

@app.get("/products")
def gets_products():
    return {
        "status" : "success",
        "message" : "Lấy danh sách sản phẩm thành công",
        "data" : products
    }

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return{
                "status" : "success",
                "message" : "Lấy sản phẩm thành công",
                "data" : product
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Không tìm thấy sản phẩm "
    )

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreated):
    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }

    products.append(new_product)

    return {
        "status": "success",
        "message": "Tạo mới sản phẩm thành công",
        "data": new_product
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            del products[index]

            return {
                "status": "success",
                "message": "Xoá sản phẩm thành công"
            }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm")
