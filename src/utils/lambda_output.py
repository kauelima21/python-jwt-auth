import json


def json_response(body, statusCode: int = 200, isBase64Encoded: bool = False):
    return {
        "isBase64Encoded": isBase64Encoded,
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body),
    }
