import logging
import json
from src.repositories.boto.boto_user_repository import BotoUserRepository
from src.services.login.use_cases.register_user import RegisterUserUseCase
from src.utils.errors.passwords_not_match import PasswordsNotMatchError
from src.utils.errors.user_already_exists import UserAlreadyExistsError
from src.utils.event import json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    if not event.get('body'):
        return None

    requestBody = json.loads(event.get('body'))
    
    logging.info(requestBody)

    user_repository = BotoUserRepository()
    register_user_use_case = RegisterUserUseCase(user_repository)
    try:
        user = register_user_use_case.execute({
            "username": requestBody["username"],
            "email": requestBody["email"],
            "password": requestBody["password"],
            "password_confirm": requestBody["password_confirm"],
        })

        logging.info(user)

        return json_response(None, 201)
    except PasswordsNotMatchError:
        return json_response({
            "message": "Passwords does not match."
        }, 400)
    except UserAlreadyExistsError:
        return json_response({
            "message": "User already exists."
        }, 409)
