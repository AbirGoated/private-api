from fastapi import FastAPI
from pydantic import BaseModel
from backend.database import get_tasks

app = FastAPI()

class Task(BaseModel):
    title: str
    completed: bool = False 


@app.get("/")
def home():
    return {"message": "Personal API is running!"}

@app.get("/tasks")
def read_tasks():
    return get_tasks()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return {"Error": "Task not found"}

@app.post("/tasks")
def create_task(task: Task):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": task.completed
    }
    tasks.append(new_task)
    return new_task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"Message": "Task deleted"}
    return {"Error": "Task not found"}

@app.put("/tasks/{task_id}")
def updated_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["completed"] = updated_task.completed
            return task
    return {"Error": "Task not found"}
