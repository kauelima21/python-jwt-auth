from abc import ABC, abstractmethod
from typing import List
from src.entities.task import Task, TaskProps


class TaskRepository(ABC):
    @abstractmethod
    def findById(self, id: str) -> Task:
        pass

    @abstractmethod
    def fetchByUser(self, user_id: str) -> List[TaskProps]:
        pass

    @abstractmethod
    def delete(self, task: Task) -> Task:
        pass

    @abstractmethod
    def complete(self, task: Task) -> Task:
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    def save(self, task: Task) -> Task:
        pass
