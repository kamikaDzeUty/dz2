from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

# Настройки JSONBin
BIN_ID = "67fa087c8561e97a50fde42f"
API_KEY = "$2a$10$tYTx.93q4Cf9FyU7Xtx0fuAIOhwzun91X5GJ0jkt25HmDtqMqsjie"
BASE_URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

# Настройки Cloudflare Workers AI
CF_TOKEN = "JdABwfqNvOMh1u1l9Fi96DbGjTZZI6XpgB5cxo-P"
ACCOUNT_ID = "a9061e0592798bdf20f49728102d1432"


class Task(BaseModel):
    id: int
    name: str
    status: str


class CloudflareLLM:
    def __init__(self, token: str, account_id: str):
        self.token = token
        self.account_id = account_id
        self.model = "@cf/meta/llama-3-8b-instruct"
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def generate_solution(self, task_text: str) -> str:
        prompt = f"Объясни, как решить следующую задачу:\n{task_text}"
        body = {
            "messages": [
                {"role": "system", "content": "Ты помощник, который решает простые задачи на русском языке"},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.base_url, headers=self.headers, json=body)
        if response.status_code != 200:
            raise Exception(f"Cloudflare AI Error: {response.status_code} {response.text}")

        result = response.json()
        return result["result"]["response"]


class CloudTaskStorage:
    @staticmethod
    def load_tasks() -> List[Task]:
        response = requests.get(BASE_URL, headers=HEADERS)
        if response.status_code != 200:
            return []
        data = response.json()["record"]
        return [Task(**item) for item in data.get("tasks", [])]

    @staticmethod
    def save_tasks(tasks: List[Task]):
        data = {"tasks": [task.dict() for task in tasks]}
        requests.put(BASE_URL, headers=HEADERS, json=data)

    def get_all(self) -> List[Task]:
        return self.load_tasks()

    def add_task(self, task: Task) -> bool:
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


app = FastAPI()
storage = CloudTaskStorage()
llm = CloudflareLLM(CF_TOKEN, ACCOUNT_ID)


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return storage.get_all()

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    explanation = llm.generate_solution(task.name)
    task.name += f"\n💡 Решение от ИИ:\n{explanation}"
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
