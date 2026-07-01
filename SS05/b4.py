# 1. Phân tích Input/Output
# Input
# product_id nhận từ Path Parameter.
# Dữ liệu cập nhật nhận từ Request Body.

# Output khi thành công
# HTTP Status Code: 200 OK.
# Trả về thông tin sản phẩm sau khi cập nhật.

# Output khi thất bại

# 404 Not Found: "Product not found" nếu product_id không tồn tại.
# 400 Bad Request: "Product code already exists" nếu mã sản phẩm bị trùng.
# 422 Unprocessable Entity: Nếu name rỗng, price <= 0 hoặc stock < 0 (do Pydantic kiểm tra).

# 2. Đề xuất 2 giải pháp
# Giải pháp 1: Duyệt List
# Duyệt danh sách products để tìm sản phẩm theo product_id.
# Nếu không tìm thấy thì trả về lỗi 404.
# Duyệt lại danh sách để kiểm tra code có bị trùng với sản phẩm khác hay không.
# Nếu hợp lệ thì cập nhật thông tin sản phẩm.

# Ưu điểm
# Đơn giản, dễ hiểu.
# Phù hợp với dữ liệu nhỏ hoặc lưu trong bộ nhớ.

# Nhược điểm
# Phải duyệt danh sách nhiều lần.
# Khi dữ liệu lớn, tốc độ chậm.
# Giải pháp 2: Dùng Dictionary
# Chuyển dữ liệu sang dạng dict với product_id là khóa.
# Tìm sản phẩm bằng product_id rất nhanh.
# Khi kiểm tra trùng code, vẫn cần duyệt các sản phẩm còn lại.
# Sau khi kiểm tra hợp lệ thì cập nhật dữ liệu.

# Ưu điểm
# Tìm kiếm theo id nhanh hơn.
# Phù hợp khi số lượng dữ liệu lớn.

# Nhược điểm
# Tốn thêm bộ nhớ để lưu dict.
# Code phức tạp hơn.

# Giải pháp 1: Duyệt List
# Tốc độ tìm kiếm: Chậm hơn vì phải duyệt từng phần tử trong danh sách (độ phức tạp O(n)).
# Bộ nhớ: Ít tốn bộ nhớ vì sử dụng trực tiếp danh sách có sẵn.
# Dễ hiểu: Rất dễ hiểu, phù hợp với người mới học FastAPI.
# Dễ bảo trì: Dễ sửa đổi và bảo trì do thuật toán đơn giản.
# Bối cảnh phù hợp: Thích hợp với dữ liệu nhỏ hoặc các bài tập thực hành.

# Giải pháp 2: Dùng Dictionary
# Tốc độ tìm kiếm: Nhanh hơn vì có thể tìm sản phẩm theo id với độ phức tạp O(1).
# Bộ nhớ: Tốn nhiều bộ nhớ hơn do phải tạo thêm dict.
# Dễ hiểu: Khó hiểu hơn một chút so với duyệt list.
# Dễ bảo trì: Khá dễ bảo trì nhưng phải đồng bộ dữ liệu giữa list và dict nếu sử dụng cả hai.
# Bối cảnh phù hợp: Phù hợp với hệ thống có dữ liệu lớn và cần truy xuất thường xuyên.
# Kết luận lựa chọn
# Đối với bài toán này, nên chọn giải pháp duyệt list vì dữ liệu đang được lưu dưới dạng danh sách products,
# số lượng dữ liệu nhỏ, cách triển khai đơn giản, dễ hiểu và đáp ứng đầy đủ yêu cầu của bài tập.
# Nếu hệ thống phát triển với lượng dữ liệu lớn hoặc sử dụng cơ sở dữ liệu,
# có thể cân nhắc dùng dict hoặc truy vấn trực tiếp từ cơ sở dữ liệu để tăng hiệu năng.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]

class ProductUpdate(BaseModel):
    code: str
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):

    # Kiểm tra sản phẩm tồn tại
    product_found = None
    for product_item in products:
        if product_item["id"] == product_id:
            product_found = product_item
            break

    if product_found is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Kiểm tra trùng mã sản phẩm
    for product_item in products:
        if (
            product_item["code"] == product.code
            and product_item["id"] != product_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    # Cập nhật thông tin
    product_found["code"] = product.code
    product_found["name"] = product.name
    product_found["price"] = product.price
    product_found["stock"] = product.stock

    return {
        "message": "Update product successfully",
        "data": product_found
    }