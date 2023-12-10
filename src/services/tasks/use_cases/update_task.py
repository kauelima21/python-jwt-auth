from typing import TypedDict, Optional
from datetime import datetime
from src.repositories.task_repository import TaskRepository
from src.entities.task import Task
from src.utils.errors.resource_not_found import ResourceNotFoundError


class UpdateTaskUseCaseRequest(TypedDict):
  id: str
  title: Optional[str]
  description: Optional[str]


class UpdateTaskUseCase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self._task_repository = task_repository

    def execute(self, request: UpdateTaskUseCaseRequest):
        task = self._task_repository.findById(request["id"])

        if not task:
            raise ResourceNotFoundError("Resource Not Found")

        task["title"] = request.get("title") if request.get("title") else task["title"]
        task["description"] = request.get("description") if request.get("description") else task["description"]

        return self._task_repository.update(task)
