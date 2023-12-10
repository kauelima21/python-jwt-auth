import json
import pytest
from moto import mock_dynamodb
from src.infra.create_tasks_table import create_table
from src.services.tasks.handlers.update import lambda_handler
from tests.fixtures.tasks import populate_moto_table


@pytest.fixture()
def event():
    event = {
      "pathParameters": {
        "id": "1cedb5f6-c0b8-4cd3-ab1b-47089c113614"
      },
      "body": "{\"title\": \"Minha Task Atualizada\"}",
    }
    yield event


@mock_dynamodb
def test_it_shoud_be_able_to_update_a_task(event, populate_moto_table):
    create_table()
    populate_moto_table(event["pathParameters"]["id"])
    response = lambda_handler(event, None)
    task = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert task.get("title") == json.loads(event["body"]).get("title")


if __name__ == "__main__":
    pytest.main()
