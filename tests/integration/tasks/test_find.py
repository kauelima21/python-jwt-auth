import json
import pytest
from src.handlers.tasks.find import lambda_handler


@pytest.fixture()
def event():
    event = {
      "pathParameters": {
        "id": "1cedb5f6-c0b8-4cd3-ab1b-47089c113614"
      }
    }
    yield event


@pytest.mark.skip
def test_it_shoud_be_able_to_find_a_task(event):
    response = lambda_handler(event, None)
    tasks = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert tasks.get("id") == event["pathParameters"]["id"]


if __name__ == "__main__":
    pytest.main()
