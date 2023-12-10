from datetime import datetime
import uuid
import pytest
import boto3


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
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
          }
        )
    return populate
