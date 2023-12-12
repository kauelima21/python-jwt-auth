import pytest
from src.repositories.in_memory.in_memory_user_repository import InMemoryUserRepository
from src.services.login.use_cases.register_user import RegisterUserUseCase
from src.utils.errors.passwords_not_match import PasswordsNotMatchError
from src.utils.errors.user_already_exists import UserAlreadyExistsError


@pytest.fixture()
def user_repository():
    user_repository = InMemoryUserRepository()
    user_repository.save({
        "id": "id-1",
        "username": "sanji",
        "email": "kaue@email.com",
        "password_hash": "mypassword123",
    })
    yield user_repository


@pytest.fixture()
def user_data():
    user_data = {
        "username": "sanji",
        "email": "kaue@email.com",
        "password": "mypassword123",
        "password_confirm": "mypassword123",
    }
    yield user_data


def test_it_shoud_be_able_to_register_an_user(user_data):
    user_repository = InMemoryUserRepository()
    register_user_use_case = RegisterUserUseCase(user_repository)
    user = register_user_use_case.execute({
        "username": user_data["username"],
        "email": user_data["email"],
        "password": user_data["password"],
        "password_confirm": user_data["password_confirm"],
    })

    assert user.username == user_data["username"]
    assert user.email == user_data["email"]


def test_it_shoud_not_be_able_to_register_an_user_with_non_match_passwords(user_data):
    user_repository = InMemoryUserRepository()
    register_user_use_case_request = {
        "username": user_data["username"],
        "email": user_data["email"],
        "password": user_data["password"],
        "password_confirm": "outrasenha",
    }

    with pytest.raises(PasswordsNotMatchError) as err:
        RegisterUserUseCase(user_repository).execute(register_user_use_case_request)
    assert str(err.value) == "password and password_confirm should be equal."


def test_it_shoud_not_be_able_to_register_an_user_with_existing_email(user_data, user_repository):
    register_user_use_case_request = {
        "username": "john.doe",
        "email": user_data["email"],
        "password": user_data["password"],
        "password_confirm": user_data["password_confirm"],
    }

    with pytest.raises(UserAlreadyExistsError) as err:
        RegisterUserUseCase(user_repository).execute(register_user_use_case_request)
    assert str(err.value) == "User already exists."


def test_it_shoud_not_be_able_to_register_an_user_with_existing_username(user_data, user_repository):
    register_user_use_case_request = {
        "username": user_data["username"],
        "email": "john.doe@email.com",
        "password": user_data["password"],
        "password_confirm": user_data["password_confirm"],
    }

    with pytest.raises(UserAlreadyExistsError) as err:
        RegisterUserUseCase(user_repository).execute(register_user_use_case_request)
    assert str(err.value) == "User already exists."


if __name__ == "__main__":
    pytest.main()
