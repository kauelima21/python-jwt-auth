import json
import pytest
from moto import mock_dynamodb
from src.services.tasks.handlers.fetch import lambda_handler
from tests.fixtures.tasks import populate_moto_table
from src.infra.create_tasks_table import create_table


@pytest.fixture()
def event():
    event = {}
    yield event


@mock_dynamodb
def test_it_shoud_be_able_to_fetch_tasks(event, populate_moto_table):
    create_table()
    populate_moto_table(None)
    response = lambda_handler(event, None)
    tasks = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert type(tasks) == list
    assert len(tasks) == 1


if __name__ == "__main__":
    pytest.main()
