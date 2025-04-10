from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    name: str
    status: str


tasks: List[Task] = []

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    if any(t.id == task.id for t in tasks):
        raise HTTPException(status_code=400, detail='Задача с таким ID уже существует')
    tasks.append(task)
    return f'Задача {task} была добавлена'

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, new_task:Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = new_task
            return f'Задача обновилась на {new_task}'
    raise HTTPException(status_code=404, detail='Такой задачи нет')
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return 'Задача удалена'
    raise HTTPException(status_code=404, detail='Такой задачи нет')
# Сервер запустился, всё файн 👍💕