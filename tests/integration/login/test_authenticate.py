import pytest
import boto3
import json
from moto import mock_dynamodb, mock_secretsmanager
from src.infra.create_users_table import create_table
from src.services.login.handlers.authenticate import lambda_handler
from tests.fixtures.login import populate_moto_table


@pytest.fixture()
def valid_event():
    event = {
      "body": "{\"email\": \"kaue@email.com\", \"password\": \"mypassword123\"}",
    }
    yield event


@pytest.fixture()
def invalid_event():
    event = {
      "body": "{\"email\": \"sanji@mail.com\", \"password\": \"mypassword123\"}",
    }
    yield event


@mock_secretsmanager
@mock_dynamodb
def test_it_shoud_be_able_to_authenticate_an_user(valid_event, populate_moto_table):
    create_table()
    populate_moto_table(id=None)

    client = boto3.client("secretsmanager", region_name="sa-east-1")
    secret_string = json.dumps({
        "jwt_secret_key": "secret"
    })
    client.create_secret(Name="dev/jwt_key", SecretString=secret_string)

    response = lambda_handler(valid_event, None)

    assert response["statusCode"] == 200


@mock_secretsmanager
@mock_dynamodb
def test_it_shoud_not_be_able_to_authenticate_an_user(invalid_event, populate_moto_table):
    create_table()
    populate_moto_table(id=None)

    response = lambda_handler(invalid_event, None)

    assert response["statusCode"] == 400


if __name__ == "__main__":
    pytest.main()
