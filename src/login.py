import jwt
from datetime import datetime, timezone, timedelta


def jwt_encode(username: str) -> dict:
    """ put this in another place 
    if not user.find_by_username(username):
        return { "authenticated": False }

    if not password == user.password:
        return { "authenticated": False }
     """
    payload = {
        "username": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=10), 
        "iat": datetime.now(tz=timezone.utc) 
    }
    key = "secret_key"

    encoded = jwt.encode(payload, key, algorithm="HS256")
    return { "authenticated": True, "jwt": encoded, "key": key }


def jwt_decode(jwt_token: str, key: str) -> bool:
    try :
        decoded = jwt.decode(jwt_token, key, algorithms=["HS256"])
        return True
    except Exception as e:
        print(e)
        return False

