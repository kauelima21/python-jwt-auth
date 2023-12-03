import pytest
from src.handlers.tasks.create import lambda_handler


@pytest.fixture()
def event():
    event = {
      "body": "{\"title\": \"Minha Task\", \"description\": \"Task Legal\"}",
    }
    yield event


def test_it_shoud_be_able_to_create_a_task(event):
    response = lambda_handler(event, None)

    assert response["statusCode"] == 201


if __name__ == "__main__":
    pytest.main()
