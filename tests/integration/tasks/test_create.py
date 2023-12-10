import pytest
from moto import mock_dynamodb
from src.infra.create_tasks_table import create_table
from src.services.tasks.handlers.create import lambda_handler


@pytest.fixture()
def event():
    event = {
      "body": "{\"title\": \"Minha Task\", \"description\": \"Task Legal\"}",
    }
    yield event


@mock_dynamodb
def test_it_shoud_be_able_to_create_a_task(event):
    create_table()
    response = lambda_handler(event, None)

    assert response["statusCode"] == 201


if __name__ == "__main__":
    pytest.main()
