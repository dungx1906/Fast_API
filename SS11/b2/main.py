from fastapi import FastAPI, Depends, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from b2.database import engine, Base, get_db
from b2.model import SmartHomePlanModel
from b2.user_service import SmartHomePlanCreate, StandardResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/smart-home-plans", status_code=status.HTTP_201_CREATED)
def create_smart_home_plan(
    request: Request,
    plan_data: SmartHomePlanCreate,
    db: Session = Depends(get_db)
):
    db_plan = SmartHomePlanModel(
        plan_code=plan_data.plan_code,
        plan_name=plan_data.plan_name,
        device_quantity=plan_data.device_quantity,
        price=plan_data.price
    )
    
    try:
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
    except IntegrityError:
        db.rollback() 
        return StandardResponse(
            statusCode=status.HTTP_400_BAD_REQUEST,
            message="Plan code already exists",
            error="Bad Request",
            data=None,
            path=request.url.path
        )
    except Exception as e:
        db.rollback() 
        return StandardResponse(
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Lỗi hệ thống khi lưu trữ dữ liệu.",
            error=str(e),
            data=None,
            path=request.url.path
        )

    plan_response_data = {
        "id": db_plan.id,
        "plan_code": db_plan.plan_code,
        "plan_name": db_plan.plan_name,
        "device_quantity": db_plan.device_quantity,
        "price": db_plan.price
    }
    return StandardResponse(
        statusCode=201,
        message="Thêm gói thiết bị thành công",
        error=None,
        data=plan_response_data,
        path=request.url.path
    )


@app.get("/smart-home-plans")
def get_all_smart_home_plans(request: Request, db: Session = Depends(get_db)):
    plans = db.query(SmartHomePlanModel).all()
    
    list_data = [
        {
            "id": plan.id,
            "plan_code": plan.plan_code,
            "plan_name": plan.plan_name,
            "device_quantity": plan.device_quantity,
            "price": plan.price
        }
        for plan in plans
    ]
    
    return StandardResponse(
        statusCode=200,
        message="Lấy danh sách thành công",
        error=None,
        data=list_data,
        path=request.url.path
    )


@app.get("/smart-home-plans/{plan_id}")
def get_smart_home_plan_detail(
    plan_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    plan = db.query(SmartHomePlanModel).filter(SmartHomePlanModel.id == plan_id).first()
    

    if plan is None:
        return StandardResponse(
            statusCode=404,
            message="Plan not found",
            error="Not Found",
            data=None,
            path=request.url.path
        )
        
    plan_response_data = {
        "id": plan.id,
        "plan_code": plan.plan_code,
        "plan_name": plan.plan_name,
        "device_quantity": plan.device_quantity,
        "price": plan.price
    }
    return StandardResponse(
        statusCode=200,
        message="Lấy thông tin chi tiết thành công",
        error=None,
        data=plan_response_data,
        path=request.url.path
    )