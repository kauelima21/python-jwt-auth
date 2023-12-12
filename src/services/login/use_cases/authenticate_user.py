from typing import TypedDict
from src.repositories.user_repository import UserRepository
from src.utils.errors.passwords_not_match import PasswordsNotMatchError
from src.utils.errors.resource_not_found import ResourceNotFoundError
from src.utils.jwt import check_bcrypt


class AuthenticateUserUseCaseRequest(TypedDict):
    email: str
    password: str


class AuthenticateUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def execute(self, request: AuthenticateUserUseCaseRequest):
        user_by_email = self._user_repository.findByEmail(request["email"])

        if not user_by_email:
            raise ResourceNotFoundError("Resource not found.")

        does_passwords_match = check_bcrypt(
          request["password"],
          user_by_email.password_hash
        )

        if not does_passwords_match:
          raise PasswordsNotMatchError("passwords does not match.")

        return user_by_email
