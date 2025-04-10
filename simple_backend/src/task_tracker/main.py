from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

data_tasks = 'tasks.json'

class Task(BaseModel):
    id: int
    name: str
    status: str

class TaskStorage:
    def __init__(self, filename: str):
        self.filename = filename

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
        return [Task(**item) for item in data]

    def save_tasks(self, tasks: List[Task]):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.dict() for task in tasks], f, indent=2, ensure_ascii=False)

    def get_all(self) -> List[Task]:
        return self.load_tasks()

    def add_task(self, task: Task):
        tasks = self.load_tasks()
        if any(t.id == task.id for t in tasks):
            return False
        tasks.append(task)
        self.save_tasks(tasks)
        return True

    def update_task(self, task_id: int, new_task: Task) -> bool:
        tasks = self.load_tasks()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                tasks[index] = new_task
                self.save_tasks(tasks)
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        tasks = self.load_tasks()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                del tasks[index]
                self.save_tasks(tasks)
                return True
        return False

storage = TaskStorage(data_tasks)

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return storage.get_all()

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    success = storage.add_task(task)
    if not success:
        raise HTTPException(status_code=400, detail="Задача с таким ID уже существует")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, new_task: Task):
    success = storage.update_task(task_id, new_task)
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    success = storage.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return 'Задача удалена'
# Сервер запустился, всё файн 👍💕
