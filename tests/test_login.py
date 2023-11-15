import pytest
from src.login import jwt_decode, jwt_encode


@pytest.fixture()
def user_data():
    user_data = {
        "username": "sanji2k",
        "password": "123"
    }
    yield user_data


def test_it_shoud_encode_successfully(user_data):
    response = jwt_encode(user_data["username"])

    assert response["authenticated"] == True


def test_it_shoud_decode_successfully(user_data):
    encoded = jwt_encode(user_data["username"])
    response = jwt_decode(encoded["jwt"], encoded["key"])

    assert response == True


if __name__ == "__main__":
    pytest.main()

