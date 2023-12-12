import pytest
from moto import mock_dynamodb
from src.infra.create_users_table import create_table
from src.services.login.handlers.register import lambda_handler
from tests.fixtures.login import populate_moto_table


@pytest.fixture()
def event():
    event = {
      "body": "{\"username\": \"sanji2k\", \"email\": \"kaue@email.com\", \"password\": \"mypassword123\", \"password_confirm\": \"mypassword123\"}",
    }
    yield event


@mock_dynamodb
def test_it_shoud_be_able_to_register_an_user(event):
    create_table()
    response = lambda_handler(event, None)

    assert response["statusCode"] == 201


@mock_dynamodb
def test_it_shoud_not_be_able_to_register_an_existing_user(event, populate_moto_table):
    create_table()
    populate_moto_table(id=None)

    response = lambda_handler(event, None)

    assert response["statusCode"] == 409


if __name__ == "__main__":
    pytest.main()
