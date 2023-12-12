from typing import TypedDict
from datetime import datetime
from src.repositories.user_repository import UserRepository
from src.entities.user import User
from src.utils.errors.passwords_not_match import PasswordsNotMatchError
from src.utils.errors.user_already_exists import UserAlreadyExistsError
from src.utils.jwt import hash_bcrypt


class RegisterUserUseCaseRequest(TypedDict):
    username: str
    email: str
    password: str
    password_confirm: str


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def execute(self, request: RegisterUserUseCaseRequest):
        if request["password"] != request["password_confirm"]:
            raise PasswordsNotMatchError("password and password_confirm should be equal.")

        user_by_email = self._user_repository.findByEmail(request["email"])
        user_by_username = self._user_repository.findByUsername(request["username"])

        if user_by_email or user_by_username:
            raise UserAlreadyExistsError("User already exists.")

        password_hash = hash_bcrypt(request["password"])

        user = User({
          "username": request["username"],
          "email": request["email"],
          "password_hash": password_hash,
          "created_at": datetime.now(),
          "updated_at": datetime.now(),
        })

        return self._user_repository.save(user)
