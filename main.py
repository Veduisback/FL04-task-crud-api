from auth import router as auth_router
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from protected import router as protected_router
app = FastAPI( 
    title="Task API",
    description="A simple in-memory CRUD API built with FastAPI.",
    version="1.0"
)
app.include_router(auth_router)
app.include_router(protected_router)
# In-memory task storage
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Test with Swagger", "done": False},
]


# Request model for creating and updating a task
class TaskCreate(BaseModel):
    title: str


# Convert FastAPI validation errors from 422 to 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Title is required"}
    )


# Root endpoint
@app.get(
    "/",
    summary="API information",
    description="Returns basic information about the Task API."
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# Health check
@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the API is running."
)
def health():
    return {"status": "ok"}


# Get all tasks
@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns all tasks currently stored in memory."
)
def get_tasks():
    return tasks


# Get one task
@app.get(
    "/tasks/{task_id}",
    summary="Get a task",
    description="Returns a single task by its ID."
)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


# Create a new task
@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task. The title must not be empty."
)
def create_task(task_data: TaskCreate):
    title = task_data.title.strip()

    if not title:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    new_task = {
        "id": max(task["id"] for task in tasks) + 1 if tasks else 1,
        "title": title,
        "done": False,
    }

    tasks.append(new_task)

    return new_task


# Update a task
@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title of an existing task."
)
def update_task(task_id: int, task_data: TaskCreate):
    for task in tasks:
        if task["id"] == task_id:
            title = task_data.title.strip()

            if not title:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Title is required and cannot be empty"}
                )

            task["title"] = title

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


# Delete a task
@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes an existing task. Returns 204 when successful."
)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )