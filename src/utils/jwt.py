import jwt
import json
import bcrypt
import boto3
from boto3.dynamodb.types import Binary
from datetime import datetime, timedelta


__secret_name__ = "dev/jwt_key"


def hash_bcrypt(string: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(string.encode("utf-8"), salt)
    return hashed


def check_bcrypt(string: str, hashed_string) -> bool:
    if type(hashed_string) == Binary:
        hashed_string = hashed_string.value
    return bcrypt.checkpw(string.encode("utf-8"), hashed_string)


def get_jwt_secret_key() -> str:
    client = boto3.client(
      service_name="secretsmanager",
      region_name="sa-east-1"
    )

    secret_value = client.get_secret_value(SecretId=__secret_name__)
    secret_string = json.loads(secret_value.get("SecretString"))
    return secret_string.get("jwt_secret_key")


def jwt_sign(payload: dict, expiration_hours=1):
    exp = datetime.now() + timedelta(hours=expiration_hours)
    secret_string = get_jwt_secret_key()
    payload["exp"] = int(exp.timestamp())
    token = jwt.encode(payload, secret_string, algorithm="HS256")
    return token


def jwt_verify(token: str):
    secret_string = get_jwt_secret_key()
    decoded_token = jwt.decode(token, secret_string, algorithms=["HS256"])
    return decoded_token
