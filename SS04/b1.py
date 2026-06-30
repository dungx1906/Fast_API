# 1. Khi gọi GET /products/1, vì sao API trả về 404 Not Found?
# Vì route đang được khai báo là "/products/product_id" (đường dẫn cố định), 
# nên FastAPI chỉ chấp nhận URL /products/product_id. Khi gọi /products/1, không có route nào khớp nên trả về 404 Not Found.

# 2. Dòng code nào đang khai báo sai Path Parameter?
# @app.get("/products/product_id")

# 3. Vì sao /products/product_id không phải là Path Parameter?
# Vì product_id không được đặt trong dấu {}. FastAPI hiểu product_id là một chuỗi cố định trong URL, không phải là biến nhận giá trị từ đường dẫn.

# 4. Endpoint đúng cần sửa thành gì?
# @app.get("/products/{product_id}")
# Khi đó, lời gọi:
# GET /products/1
# sẽ truyền giá trị 1 vào tham số:
# def get_product_detail(product_id: int):
# để tìm và trả về thông tin sản phẩm có id = 1.

from fastapi import FastAPI
app = FastAPI()
products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000}
]
@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {
        "message": "Không tìm thấy sản phẩm"
    }