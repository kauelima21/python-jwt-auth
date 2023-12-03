from src.repositories.task_repository import TaskRepository
from src.use_cases.errors.resource_not_found import ResourceNotFoundError


class DeleteTaskUseCase:
  def __init__(self, task_repository: TaskRepository) -> None:
    self._task_repository = task_repository

  def execute(self, task_id: str):
    task = self._task_repository.findById(task_id)

    if not task:
      raise ResourceNotFoundError("Resource Not Found")

    return self._task_repository.delete(task_id)
