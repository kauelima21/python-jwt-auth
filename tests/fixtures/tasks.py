import uuid
import pytest
import boto3
from datetime import datetime
from src.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository


@pytest.fixture()
def task_repository():
    task_repository = InMemoryTaskRepository()
    task_repository.save({
        "id": "id-1",
        "title": "My Task 01",
        "description": "This is my first task.",
        "user_id": str(uuid.uuid4()),
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    })
    task_repository.save({
        "id": "id-2",
        "title": "My Task 02",
        "description": "This is my second task.",
        "user_id": "my-user",
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    })
    task_repository.save({
        "id": "id-3",
        "title": "My Task 03",
        "description": "This is my third task.",
        "user_id": "my-user",
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    })
    yield task_repository


@pytest.fixture()
def populate_moto_table():
    def populate(id):
        resource = boto3.resource("dynamodb")
        table = resource.Table("tasks")
        task_id = id if id else str(uuid.uuid4())
        table.put_item(
          Item={
            "id": task_id,
            "title": "My Task",
            "description": "This is my task.",
            "user_id": "my-user",
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
          }
        )
    return populate
