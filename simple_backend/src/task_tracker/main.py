from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI()

data_tasks = 'tasks.json'

class Task(BaseModel):
    id: int
    name: str
    status: str

def load_tasks():
    if not os.path.exists(data_tasks):
        return []
    with open(data_tasks, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return [Task(**item) for item in data]
        except json.JSONDecodeError:
            return []

def save_tasks(tasks: List[Task]):
    with open(data_tasks, "w", encoding="utf-8") as f:
        json.dump([task.dict() for task in tasks], f, indent=2, ensure_ascii=False)

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return load_tasks()

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks = load_tasks()
    if any(t.id == task.id for t in tasks):
        raise HTTPException(status_code=400, detail='Задача с таким ID уже существует')
    tasks.append(task)
    save_tasks(tasks)
    return f'Задача {task} была добавлена'

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, new_task:Task):
    tasks = load_tasks()
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = new_task
            save_tasks(tasks)
            return f'Задача обновилась на {new_task}'
    raise HTTPException(status_code=404, detail='Такой задачи нет')

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            save_tasks(tasks)
            return 'Задача удалена'
    raise HTTPException(status_code=404, detail='Такой задачи нет')
# Сервер запустился, всё файн 👍💕
