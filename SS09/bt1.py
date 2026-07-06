from datetime import datetime, timezone
from typing import Any, List, Optional, Tuple
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class UnifiedResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str
    path: str

    @classmethod
    def send(
        cls,
        status_code: int,
        message: str,
        data: Any = None,
        error: str = None,
        path: str = "",
    ):
        if error is not None:
            data = None

        envelope = cls(
            statusCode=status_code,
            message=message,
            data=data,
            error=error,
            timestamp=datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            path=path,
        )
        return JSONResponse(status_code=status_code, content=envelope.model_dump())


class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=1)
    priority: int = Field(..., ge=1, le=5)

    @classmethod
    def model_validate(cls, *args, **kwargs):
        obj = super().model_validate(*args, **kwargs)
        obj.assignee = obj.assignee.strip()
        return obj


class TaskStatusUpdateSchema(BaseModel):
    status: str = Field(..., pattern="^(todo|in_progress|done)$")


tasks_db = [
    {
        "id": 1,
        "title": "Thiet ke database Shop AI",
        "description": "Xay dung bang va toi uu index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z",
    },
    {
        "id": 2,
        "title": "Code bo API Authen",
        "description": "Trien khai filter verify JWT token",
        "assignee": "FixerQ",
        "priority": 2,
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z",
    },
]

app = FastAPI(title="Team Task Management API")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return UnifiedResponse.send(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
        error="ERR-VAL-422: Validation error at Request Body fields constraint layout.",
        path=request.url.path,
    )


@app.exception_handler(Exception)
async def global_runtime_exception_handler(request: Request, exc: Exception):
    return UnifiedResponse.send(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Hệ thống gặp sự cố nghiêm trọng, vui lòng thử lại sau.",
        error=f"INTERNAL_SERVER_ERROR: {str(exc)}",
        path=request.url.path,
    )


def calculate_team_metrics() -> Tuple[int, int, float]:
    total_tasks = len(tasks_db)
    if total_tasks == 0:
        return (0, 0, 0.0)

    completed_tasks = sum(1 for task in tasks_db if task["status"] == "done")
    completion_rate_percentage = round((completed_tasks / total_tasks) * 100, 2)

    return (total_tasks, completed_tasks, completion_rate_percentage)


@app.get("/tasks")
async def get_all_tasks(request: Request, status: Optional[str] = None):
    if status:
        filtered_tasks = [task for task in tasks_db if task["status"] == status]
    else:
        filtered_tasks = tasks_db

    return UnifiedResponse.send(
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách công việc thành công!",
        data=filtered_tasks,
        path=request.url.path,
    )


@app.post("/tasks")
async def create_task(request: Request, task_in: TaskCreateSchema):
    for task in tasks_db:
        if task["title"].strip() == task_in.title.strip():
            return UnifiedResponse.send(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                error="ERR-TASK-01: Task conflict: Title field duplicates an existing record.",
                path=request.url.path,
            )

    max_id = max([task["id"] for task in tasks_db]) if tasks_db else 0
    new_id = max_id + 1

    new_task = {
        "id": new_id,
        "title": task_in.title,
        "description": task_in.description,
        "assignee": task_in.assignee,
        "priority": task_in.priority,
        "status": "todo",
        "created_at": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
    }

    tasks_db.append(new_task)

    return UnifiedResponse.send(
        status_code=status.HTTP_201_CREATED,
        message="Khởi tạo công việc mới thành công!",
        data=new_task,
        path=request.url.path,
    )


@app.put("/tasks/{task_id}")
async def update_task_status(
    request: Request, task_id: int, status_in: TaskStatusUpdateSchema
):
    target_task = None
    for task in tasks_db:
        if task["id"] == task_id:
            target_task = task
            break

    if not target_task:
        return UnifiedResponse.send(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Lỗi: Không tìm thấy ID công việc yêu cầu cập nhật!",
            error="ERR-TASK-03: Task target not found: The requested task ID does not exist.",
            path=request.url.path,
        )

    if target_task["status"] == "done":
        return UnifiedResponse.send(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Lỗi: Không thể thay đổi trạng thái của công việc đã hoàn thành!",
            error="ERR-TASK-04: Task mutation blocked: Completed tasks cannot transition back to other states.",
            path=request.url.path,
        )

    target_task["status"] = status_in.status

    return UnifiedResponse.send(
        status_code=status.HTTP_200_OK,
        message="Cập nhật tiến độ công việc thành công!",
        data=target_task,
        path=request.url.path,
    )


@app.get("/tasks/analytics/dashboard")
async def get_dashboard_analytics(request: Request):
    total_tasks, completed_tasks, completion_rate_percentage = (
        calculate_team_metrics()
    )

    analytics_data = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate_percentage": completion_rate_percentage,
    }

    return UnifiedResponse.send(
        status_code=status.HTTP_200_OK,
        message="Lấy số liệu thống kê hiệu suất nhóm thành công!",
        data=analytics_data,
        path=request.url.path,
    )


@app.get("/tasks/debug/trigger-error")
async def trigger_runtime_error(request: Request):
    bug = 10 / 0
    return {"result": bug}