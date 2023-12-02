from src.repositories.task_repository import TaskRepository


class CompleteTaskUseCase:
  def __init__(self, task_repository: TaskRepository) -> None:
    self._task_repository = task_repository

  def execute(self, task_id: str):
    return self._task_repository.complete(task_id)
