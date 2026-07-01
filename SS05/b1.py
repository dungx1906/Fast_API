# Test case 1
# Dữ liệu gửi lên:
# {
#     "code": "SP001",
#     "name": "Laptop HP",
#     "price": 17000000,
#     "stock": 5
# }
# Kết quả hiện tại: API vẫn tạo thành công sản phẩm mới.
# Kết quả đúng mong muốn: API phải trả về lỗi 400 Bad Request với thông báo "Product code already exists".
# Lỗi phát hiện: API không kiểm tra mã sản phẩm đã tồn tại trước khi thêm vào danh sách.

# Test case 2
# Dữ liệu gửi lên:
# {
#     "code": "SP002",
#     "name": "Keyboard Logitech",
#     "price": 500000,
#     "stock": 20
# }
# Kết quả hiện tại: API vẫn tạo thành công sản phẩm mới mặc dù mã SP002 đã có trong hệ thống.
# Kết quả đúng mong muốn: API phải trả về lỗi 400 Bad Request với thông báo "Product code already exists".
# Lỗi phát hiện: Hệ thống cho phép tạo nhiều sản phẩm có cùng mã, làm dữ liệu bị trùng lặp.

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

@app.post("/products")
def create_product(product: ProductCreate):
    for product in products:
        if product["code"] == product.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product code already exists"
            )

    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }
    products.append(new_product)
    return {
        "message": "Create product successfully",
        "data": new_product
    }