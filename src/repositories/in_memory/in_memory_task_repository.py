from datetime import datetime
from typing import List
from src.entities.task import Task
from src.repositories.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._data = []

    def findById(self, id: str) -> Task:
        filtered_task = filter(lambda task: task.get("id") == id, self._data)
        task_array = list(filtered_task)
        if len(task_array) <= 0:
          return None

        return task_array[0]

    def findAll(self) -> List[Task]:
        return self._data

    def delete(self, task: Task) -> Task:
        index = 0
        task_to_delete = None

        for i, task in enumerate(self._data):
          if task.get("id") == task.get("id"):
            index = i
            task_to_delete = task

        self._data.pop(index)
        return task_to_delete

    def complete(self, task: Task) -> Task:
        index = 0
        task_to_complete = None

        for i, task in enumerate(self._data):
          if task.get("id") == task.get("id"):
            index = i
            task_to_complete = task

        task_to_complete["completed_at"] = datetime.now()
        task_to_complete["updated_at"] = datetime.now()

        self._data[index] = task_to_complete
        return task_to_complete

    def update(self, task: Task) -> Task:
        index = 0

        for i, item in enumerate(self._data):
          if item.get("id") == task.get("id"):
            index = i

        self._data[index] = task
        return task

    def save(self, task: Task) -> Task:
        self._data.append(task)
        return self._data[-1]
