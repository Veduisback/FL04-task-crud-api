from auth import router as auth_router
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from protected import router as protected_router
from dependencies import get_current_user
from fastapi import Depends
app = FastAPI( 
    title="Task API",
    description="A simple in-memory CRUD API built with FastAPI.",
    version="1.0"
)
app.include_router(auth_router)
app.include_router(protected_router)
# In-memory task storage
tasks = []


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
        content={"error": "Invalid request data"}
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
    description="Returns all tasks belonging to the authenticated user."
)
def get_tasks(current_user=Depends(get_current_user)):
    return [
        task for task in tasks
        if task["user_id"] == current_user.id
    ]

# Get one task
@app.get(
    "/tasks/{task_id}",
    summary="Get a task",
    description="Returns a single task belonging to the authenticated user."
)
def get_task(
    task_id: int,
    current_user=Depends(get_current_user)
):
    for task in tasks:
        if task["id"] == task_id and task["user_id"] == current_user.id:
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
def create_task(
    task_data: TaskCreate,
    current_user=Depends(get_current_user)
):
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
        "user_id": current_user.id,
    }
    tasks.append(new_task)

    return new_task


# Update a task
@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Updates the title of an existing task."
)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    current_user=Depends(get_current_user)
):
    for task in tasks:
        if task["id"] == task_id and task["user_id"] == current_user.id:
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
def delete_task(
    task_id: int,
    current_user=Depends(get_current_user)
):
    for task in tasks:
        if task["id"] == task_id and task["user_id"] == current_user.id:
            tasks.remove(task)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )