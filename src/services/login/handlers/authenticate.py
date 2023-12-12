import logging
import json
from datetime import datetime, timedelta
from src.repositories.boto.boto_user_repository import BotoUserRepository
from src.services.login.use_cases.authenticate_user import AuthenticateUserUseCase
from src.utils.errors.passwords_not_match import PasswordsNotMatchError
from src.utils.errors.resource_not_found import ResourceNotFoundError
from src.utils.jwt import jwt_sign
from src.utils.event import json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    if not event.get('body'):
        return None

    requestBody = json.loads(event.get('body'))

    logging.info(requestBody)

    user_repository = BotoUserRepository()
    authenticate_user_use_case = AuthenticateUserUseCase(user_repository)
    try:
        authenticated_user = authenticate_user_use_case.execute({
            "email": requestBody["email"],
            "password": requestBody["password"]
        })

        token = jwt_sign({
            "sub": authenticated_user.id,
            "username": authenticated_user.username,
        }, expiration_hours=48)

        logging.info(authenticated_user)

        return json_response(token)
    except (ResourceNotFoundError, PasswordsNotMatchError):
        return json_response({
            "message": "Invalid credentials."
        }, 400)
