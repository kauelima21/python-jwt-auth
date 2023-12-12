from datetime import datetime
from typing import List
from src.entities.task import Task, TaskProps
from src.repositories.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._data = []

    def findById(self, id: str) -> Task:
        filtered_task = filter(lambda task: task.get("id") == id, self._data)
        task_array = list(filtered_task)
        if len(task_array) <= 0:
          return None

        return Task(task_array[0], task_array[0]["id"])

    def fetchByUser(self, user_id: str) -> List[TaskProps]:
        filtered_task = filter(lambda task: task.get("user_id") == user_id, self._data)
        task_array = list(filtered_task)
        if len(task_array) <= 0:
          return None

        return task_array

    def delete(self, task: Task) -> Task:
        index = 0

        for i, item in enumerate(self._data):
          if item.get("id") == task.id:
            index = i

        self._data.pop(index)
        return task

    def complete(self, task: Task) -> Task:
        index = 0
        task_to_complete = None

        for i, item in enumerate(self._data):
          if item.get("id") == task.id:
            index = i
            task_to_complete = item

        task_to_complete["completed_at"] = datetime.now()
        task_to_complete["updated_at"] = datetime.now()

        self._data[index] = task_to_complete
        return Task(task_to_complete, task_to_complete["id"])

    def update(self, task: Task) -> Task:
        index = 0

        for i, item in enumerate(self._data):
          if item.get("id") == task.id:
            index = i

        self._data[index] = task
        return task

    def save(self, task: Task) -> Task:
        self._data.append(task)
        return task
