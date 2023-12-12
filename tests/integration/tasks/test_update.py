import json
import pytest
import boto3
from moto import mock_dynamodb, mock_secretsmanager
from src.infra.create_tasks_table import create_table
from src.services.tasks.handlers.update import lambda_handler
from src.utils.jwt import jwt_sign
from tests.fixtures.tasks import populate_moto_table


@pytest.fixture()
def event():
    event = {
        "pathParameters": {
            "id": "1cedb5f6-c0b8-4cd3-ab1b-47089c113614"
        },
        "body": "{\"title\": \"Minha Task Atualizada\"}",
        "headers": {}
    }
    yield event


@mock_secretsmanager
@mock_dynamodb
def test_it_shoud_be_able_to_update_a_task(event, populate_moto_table):
    create_table()
    populate_moto_table(event["pathParameters"]["id"])

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
    task = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert task.get("title") == json.loads(event["body"]).get("title")


if __name__ == "__main__":
    pytest.main()
