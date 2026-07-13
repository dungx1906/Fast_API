from fastapi import FastAPI
from b1.database import engine, Base
from b1.routers import product

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product Management API",
    description="Hệ thống API quản lý sản phẩm cho cửa hàng",
    version="1.0.0"
)

app.include_router(product.router)

@app.get("/")
def root():
    return {"message": "Welcome to Product Management API. Go to /docs for Swagger UI."}