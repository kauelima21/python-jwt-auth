import json
import pytest
from src.handlers.tasks.fetch import lambda_handler


@pytest.fixture()
def event():
    event = {}
    yield event


def test_it_shoud_be_able_to_fetch_tasks(event):
    response = lambda_handler(event, None)
    tasks = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert type(tasks) == list


if __name__ == "__main__":
    pytest.main()
