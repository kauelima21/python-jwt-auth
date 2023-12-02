from typing import List
from src.entities.task import Task
from src.repositories.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
  def __init__(self) -> None:
    self._data = []

  def findAll(self) -> List[Task]:
    return self._data

  def save(self, task: Task) -> Task:
    self._data.append(task)
    return self._data[-1]
