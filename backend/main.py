import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.database import get_tasks, get_task, create_task, delete_task, update_task

app = FastAPI()

class Task(BaseModel):
    title: str
    completed: bool = False
    project_id: int | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
    project_id: int | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    completed: bool = False
    project_id: int | None = None
    project_name: str | None = None


@app.get("/tasks", response_model=list[TaskOut])
def read_tasks():
    return get_tasks()

@app.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task

@app.post("/tasks", response_model=TaskOut)
def create_new_task(task: Task):
    try:
        task_id = create_task(task.title, task.project_id)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="project_id does not exist")
    return get_task(task_id)

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    rows_deleted = delete_task(task_id)
    if rows_deleted == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_existing_task(task_id: int, task: TaskUpdate):
    updates = task.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    try:
        rows_updated = update_task(task_id, **updates)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="project_id does not exist")
    if rows_updated == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return get_task(task_id)