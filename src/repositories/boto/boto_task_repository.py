from datetime import datetime
from typing import List
from src.entities.task import Task
from src.repositories.task_repository import TaskRepository
from botocore.exceptions import ClientError
import boto3


class BotoTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._data = []
        self._resource = boto3.resource(
          "dynamodb",
          region_name="us-east-1",
          endpoint_url="http://localhost:4566"
        )
        self._table = self._resource.Table("tasks")

    def findById(self, id: str) -> Task:
      filtered_task = filter(lambda task: task.get("id") == id, self._data)
      task_array = list(filtered_task)
      if len(task_array) <= 0:
        return None

      return task_array[0]

    def findAll(self) -> List[Task]:
        return self._table.scan()["Items"]

    def delete(self, id: str) -> Task:
      index = 0
      task_to_delete = None

      for i, task in enumerate(self._data):
        if task.get("id") == id:
          index = i
          task_to_delete = task

      self._data.pop(index)
      return task_to_delete

    def complete(self, id: str) -> Task:
      index = 0
      task_to_complete = None

      for i, task in enumerate(self._data):
        if task.get("id") == id:
          index = i
          task_to_complete = task

      task_to_complete["validated_at"] = datetime.now()
      task_to_complete["updated_at"] = datetime.now()

      self._data[index] = task_to_complete
      return task_to_complete

    def update(self, task: Task) -> Task:
      index = 0

      for i, item in enumerate(self._data):
        if item.get("id") == id:
          index = i

      self._data[index] = task
      return task

    def save(self, task: Task) -> Task:
      try:
          self._table.put_item(
              Item={
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "created_at": str(task.created_at),
                "updated_at": str(task.updated_at),
              }
          )
      except ClientError:
          return False

      return task
