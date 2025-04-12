from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

BIN_ID = "67fa087c8561e97a50fde42f"
API_KEY = "$2a$10$tYTx.93q4Cf9FyU7Xtx0fuAIOhwzun91X5GJ0jkt25HmDtqMqsjie"
BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

app = FastAPI()

class Task(BaseModel):
    id: int
    name: str
    status: str

class CloudTaskStorage:

    @staticmethod
    def load_tasks() -> List[Task]:
        response = requests.get(BASE_URL, headers=HEADERS)
        if response.status_code != 200:
            return []
        data = response.json()["record"]
        tasks_data = data.get("tasks", [])
        return [Task(**item) for item in tasks_data]

    @staticmethod
    def save_tasks(tasks: List[Task]):
        data = {"tasks": [task.dict() for task in tasks]}
        requests.put(BASE_URL, headers=HEADERS, json=data)

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

storage = CloudTaskStorage()

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
    return {"message": "Задача удалена"}
