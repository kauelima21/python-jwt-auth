from typing import TypedDict
from datetime import datetime
from src.repositories.task_repository import TaskRepository
from src.entities.task import Task


class CreateTaskUseCaseRequest(TypedDict):
    title: str
    description: str


class CreateTaskUseCase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, request: CreateTaskUseCaseRequest):
        task = Task({
          "title": request["title"],
          "description": request["description"],
          "created_at": datetime.now(),
          "updated_at": datetime.now(),
        })

        return self._task_repository.save(task)
