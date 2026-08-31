from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from postgres_repository import PostgresTaskRepository
from service import TaskService


load_dotenv()


app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple PostgreSQL-backed CRUD API built with FastAPI."
)


repository = PostgresTaskRepository()
service = TaskService(repository)


class TaskCreate(BaseModel):
    title: str


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Title is required"}
    )


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns all tasks stored in the PostgreSQL database."
)
def get_tasks():
    return service.get_tasks()


@app.get(
    "/tasks/{task_id}",
    summary="Get a task",
    description="Returns one task from the PostgreSQL database."
)
def get_task(task_id: int):
    task = service.get_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return task


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task and stores it in the PostgreSQL database."
)
def create_task(task_data: TaskCreate):
    title = task_data.title.strip()

    if not title:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    return service.create_task(title)


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates a task in the PostgreSQL database."
)
def update_task(task_id: int, task_data: TaskCreate):
    title = task_data.title.strip()

    if not title:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    task = service.update_task(task_id, title)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task from the PostgreSQL database."
)
def delete_task(task_id: int):
    deleted = service.delete_task(task_id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return