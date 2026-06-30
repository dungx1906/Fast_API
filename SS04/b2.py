# 1. Endpoint hiện tại có Path Parameter không?
# Có. Endpoint được khai báo là:
# @app.get("/orders/status/{status}")

# 2. Path Parameter trong bài này là gì?
# Path Parameter là status.

# 3. Khi gọi /orders/status/pending, biến status nhận giá trị gì?
# Biến status sẽ nhận giá trị:
# pending

# 4. Vì sao API hiện tại trả về sai dữ liệu?
# Vì hàm không sử dụng giá trị status để lọc đơn hàng mà trả về toàn bộ danh sách orders, nên kết quả bao gồm cả các đơn hàng pending, paid và cancelled.

# 5. Dòng code nào đang khiến API bỏ qua giá trị status?
# return orders
# Dòng lệnh này trả về toàn bộ danh sách đơn hàng mà không kiểm tra giá trị của biến status.


from fastapi import FastAPI
app = FastAPI()
orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]
@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    result = []
    
    for order in orders:
        if order["status"] == status:
            result.append(order)

    return {
            "status": "success",
            "data": result
        }
        