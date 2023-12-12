import pytest
import boto3
import uuid
from datetime import datetime
from src.utils.jwt import hash_bcrypt


@pytest.fixture
def populate_moto_table():
    def populate(id):
        resource = boto3.resource("dynamodb")
        table = resource.Table("users")
        user_id = id if id else str(uuid.uuid4())
        table.put_item(
          Item={
            "id": user_id,
            "username": "sanji2k",
            "email": "kaue@email.com",
            "password_hash": hash_bcrypt("mypassword123"),
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
          }
        )
    return populate