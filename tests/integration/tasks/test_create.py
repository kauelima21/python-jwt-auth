import pytest
import boto3
import json
from moto import mock_dynamodb, mock_secretsmanager
from src.infra.create_tasks_table import create_table
from src.services.tasks.handlers.create import lambda_handler
from src.utils.jwt import jwt_sign


@pytest.fixture()
def event():
    event = {
        "body": "{\"title\": \"Minha Task\", \"description\": \"Task Legal\"}",
        "headers": {}
    }
    yield event


@mock_secretsmanager
@mock_dynamodb
def test_it_shoud_be_able_to_create_a_task(event):
    create_table()

    client = boto3.client("secretsmanager", region_name="sa-east-1")
    secret_string = json.dumps({
        "jwt_secret_key": "secret"
    })
    client.create_secret(Name="dev/jwt_key", SecretString=secret_string)

    event["headers"]["Authorization"] = "Bearer {}".format(
        jwt_sign({
            "sub": "my-user",
            "username": "sanji",
        })
    )

    response = lambda_handler(event, None)

    assert response["statusCode"] == 201


if __name__ == "__main__":
    pytest.main()
