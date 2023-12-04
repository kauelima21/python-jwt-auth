import json
import pytest
from src.handlers.tasks.update import lambda_handler


@pytest.fixture()
def event():
    event = {
      "pathParameters": {
        "id": "1cedb5f6-c0b8-4cd3-ab1b-47089c113614"
      },
      "body": "{\"title\": \"Minha Task Atualizada\"}",
    }
    yield event


@pytest.mark.skip
def test_it_shoud_be_able_to_update_a_task(event):
    response = lambda_handler(event, None)
    task = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert task.get("title") == json.loads(event["body"]).get("title")


if __name__ == "__main__":
    pytest.main()
