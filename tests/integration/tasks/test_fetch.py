import json
import pytest
import boto3
from moto import mock_dynamodb, mock_secretsmanager
from src.services.tasks.handlers.fetch import lambda_handler
from src.utils.jwt import jwt_sign
from tests.fixtures.tasks import populate_moto_table
from src.infra.create_tasks_table import create_table


@pytest.fixture()
def event():
    event = {
        "headers": {}
    }
    yield event


@mock_secretsmanager
@mock_dynamodb
def test_it_shoud_be_able_to_fetch_tasks(event, populate_moto_table):
    create_table()
    populate_moto_table(None)

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
    tasks = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert type(tasks) == list
    assert len(tasks) == 1


if __name__ == "__main__":
    pytest.main()
