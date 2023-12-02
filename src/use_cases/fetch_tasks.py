from src.repositories.task_repository import TaskRepository


class FetchTasksUseCase:
  def __init__(self, task_repository: TaskRepository) -> None:
    self._task_repository = task_repository

  def execute(self):
    return self._task_repository.findAll()
