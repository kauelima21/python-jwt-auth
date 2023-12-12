import pytest
import boto3
import json
from moto import mock_secretsmanager
from src.utils.jwt import jwt_sign, jwt_verify


@pytest.fixture()
def token_payload():
    token_payload = {
        "sub": "cc97ac30-b34d-4546-a2b2-8f746c0f9daf",
        "username": "kaue",
    }
    yield token_payload


@mock_secretsmanager
def test_it_shoud_be_able_to_verify_a_token(token_payload):
    client = boto3.client("secretsmanager", region_name="sa-east-1")
    secret_string = json.dumps({
        "jwt_secret_key": "secret"
    })
    client.create_secret(Name="dev/jwt_key", SecretString=secret_string)

    token = jwt_sign(token_payload)

    assert jwt_verify(token)


if __name__ == "__main__":
    pytest.main()
