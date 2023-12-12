import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from typing import List
from src.entities.task import Task, TaskProps
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

        task = Task(response["Items"][0], response["Items"][0]["id"])

        return task

    def fetchByUser(self, user_id: str) -> List[TaskProps]:
        response = self._table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key("user_id").eq(user_id)
        )

        return response["Items"]

    def delete(self, task: Task) -> Task:
        self._table.delete_item(Key={
            "id": task.id
        })
        return task

    def complete(self, task: Task) -> Task:
        response = self._table.update_item(
          Key={
            "id": task.id
          },
          UpdateExpression="SET completed_at = :complete",
          ExpressionAttributeValues={
              ":complete": str(datetime.now())
          },
          ReturnValues="ALL_NEW"
        )

        completed_task = response["Attributes"]
        return Task(completed_task, completed_task.get("id"))

    def update(self, task: Task) -> Task:
        response = self._table.update_item(
          Key={
            "id": task.id
          },
          UpdateExpression="SET #uat = :uat, #ti = :ti, #desc = :desc",
          ExpressionAttributeNames={
              "#uat": "updated_at",
              "#ti": "title",
              "#desc": "description",
          },
          ExpressionAttributeValues={
              ":uat": str(datetime.now()),
              ":ti": task.title,
              ":desc": task.description,
          },
          ReturnValues="ALL_NEW"
        )

        updated_task = response["Attributes"]
        return Task(updated_task, updated_task.get("id"))

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
