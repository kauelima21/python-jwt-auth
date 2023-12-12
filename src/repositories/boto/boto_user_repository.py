import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from src.entities.user import User
from src.repositories.user_repository import UserRepository
from botocore.exceptions import ClientError



class BotoUserRepository(UserRepository):
    def __init__(self) -> None:
        self._data = []
        self._resource = boto3.resource(
          "dynamodb",
          region_name="sa-east-1"
        )
        self._table = self._resource.Table("users")

    def findById(self, id: str) -> User:
        response = self._table.query(
          KeyConditionExpression=Key("id").eq(id)
        )

        if len(response["Items"]) <= 0:
          return None

        user = response["Items"][0]

        return User(user, user.get("id"))

    def findByEmail(self, email: str) -> User:
        response = self._table.query(
            IndexName="email-index",
            KeyConditionExpression=Key("email").eq(email)
        )

        if len(response["Items"]) <= 0:
            return None

        user = response["Items"][0]

        return User(user, user.get("id"))

    def findByUsername(self, username: str) -> User:
        response = self._table.query(
            IndexName="username-index",
            KeyConditionExpression=Key("username").eq(username)
        )

        if len(response["Items"]) <= 0:
          return None

        user = response["Items"][0]

        return User(user, user.get("id"))

    def validate(self, user: User) -> User:
        response = self._table.update_item(
            Key={
                "id": user.id
            },
            UpdateExpression="SET validated_at = :validate",
            ExpressionAttributeValues={
                ":validate": str(datetime.now())
            },
            ReturnValues="ALL_NEW"
        )

        user_validated = response["Attributes"]
        return User(user_validated, user_validated.get("id"))

    def save(self, user: User) -> User:
        try:
            self._table.put_item(
                Item={
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "password_hash": user.password_hash,
                    "created_at": str(user.created_at),
                    "updated_at": str(user.updated_at),
                }
            )
        except ClientError:
            return False

        return user
