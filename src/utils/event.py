import json
from src.utils.jwt import jwt_verify
from src.utils.errors.unauthorized import UnauthorizedError


def authorize_user(event) -> dict:
    authorization = event["headers"]["Authorization"]

    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Unauthorized user.")

    authorization_token = authorization.split("Bearer ")[1]
    try:
        return jwt_verify(authorization_token)
    except:
        raise UnauthorizedError("Unauthorized user.")


def json_response(body, statusCode: int = 200, isBase64Encoded: bool = False):
    return {
        "isBase64Encoded": isBase64Encoded,
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body),
    }
