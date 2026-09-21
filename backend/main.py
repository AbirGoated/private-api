from fastapi import FastAPI
from pydantic import BaseModel
from backend.database import (get_tasks, get_task, create_task, delete_task, complete_task) 

app = FastAPI()

class Task(BaseModel):
    title: str
    completed: bool = False
    project_id: int | None = None


@app.get("/tasks")
def read_tasks():
    return get_tasks()

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    task = get_task(task_id)
    if task is None:
        return{"Error": "No task found"}
    return task

@app.post("/tasks")
def create_new_task(task: Task):
    task_id=create_task(task.title, task.project_id)
    new_task = {
        "id": task_id,
        "title": task.title,
        "completed": task.completed,
        "project_id": task.project_id,
    }

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    rows_deleted = delete_task(task_id)
    if rows_deleted == 0:
        return {"error": "Task not found"}
    return {"Success!": "Task was deleted"}

@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    rows_updated = complete_task(task_id)
    if rows_updated == 0:
        return {"Error": "Task not found"}
    return {"Success": "Task completed"}