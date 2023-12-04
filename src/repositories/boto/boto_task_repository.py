import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from typing import List
from src.entities.task import Task
from src.repositories.task_repository import TaskRepository
from botocore.exceptions import ClientError


class BotoTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._data = []
        self._resource = boto3.resource(
          "dynamodb",
          region_name="sa-east-1"
        )
        self._table = self._resource.Table("tasks")

    def findById(self, id: str) -> Task:
        response = self._table.query(
          KeyConditionExpression=Key("id").eq(id)
        )

        if len(response["Items"]) <= 0:
          return None

        task = response["Items"][0]

        return task

    def findAll(self) -> List[Task]:
        return self._table.scan()["Items"]

    def delete(self, task: Task) -> Task:
        self._table.delete_item(Key={
            "id": task.get("id")
        })
        return task

    def complete(self, task: Task) -> Task:
        response = self._table.update_item(
          Key={
            "id": task.get("id")
          },
          UpdateExpression="SET completed_at = :complete",
          ExpressionAttributeValues={
              ":complete": str(datetime.now())
          },
          ReturnValues="ALL_NEW"
        )

        task_completed = response["Attributes"]
        return task_completed

    def update(self, task: Task) -> Task:
        response = self._table.update_item(
          Key={
            "id": task.get("id")
          },
          UpdateExpression="SET #uat = :uat, #ti = :ti, #desc = :desc",
          ExpressionAttributeNames={
              "#uat": "updated_at",
              "#ti": "title",
              "#desc": "description",
          },
          ExpressionAttributeValues={
              ":uat": str(datetime.now()),
              ":ti": task.get("title"),
              ":desc": task.get("description"),
          },
          ReturnValues="ALL_NEW"
        )

        task_completed = response["Attributes"]
        return task_completed

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
