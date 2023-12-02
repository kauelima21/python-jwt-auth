from abc import ABC, abstractmethod
from typing import List
from src.entities.task import Task


class TaskRepository(ABC):
  @abstractmethod
  def findById(self, id: str) -> Task:
    pass

  @abstractmethod
  def findAll(self) -> List[Task]:
    pass

  @abstractmethod
  def complete(self, id: str) -> Task:
    pass

  @abstractmethod
  def save(self, task: Task) -> Task:
    pass
