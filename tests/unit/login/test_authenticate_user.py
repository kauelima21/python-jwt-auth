import pytest
from src.repositories.in_memory.in_memory_user_repository import InMemoryUserRepository
from src.services.login.use_cases.authenticate_user import AuthenticateUserUseCase
from src.utils.errors.passwords_not_match import PasswordsNotMatchError
from src.utils.errors.resource_not_found import ResourceNotFoundError
from src.utils.jwt import hash_bcrypt


@pytest.fixture()
def user_repository():
    user_repository = InMemoryUserRepository()
    user_repository.save({
        "id": "id-1",
        "username": "sanji",
        "email": "kaue@email.com",
        "password_hash": hash_bcrypt("mypassword123"),
    })
    yield user_repository


@pytest.fixture()
def user_data():
    user_data = {
        "email": "kaue@email.com",
        "password": "mypassword123",
    }
    yield user_data


def test_it_shoud_be_able_to_authenticate_an_user(user_data, user_repository):
    authenticate_user_use_case = AuthenticateUserUseCase(user_repository)
    authenticated_user = authenticate_user_use_case.execute({
        "email": user_data["email"],
        "password": user_data["password"],
    })

    assert authenticated_user


def test_it_shoud_not_be_able_to_authenticate_an_user_with_non_match_passwords(user_data, user_repository):
    authenticate_user_use_case_request = {
        "email": user_data["email"],
        "password": "anotherpass",
    }

    with pytest.raises(PasswordsNotMatchError) as err:
        AuthenticateUserUseCase(user_repository).execute(authenticate_user_use_case_request)
    assert str(err.value) == "passwords does not match."


def test_it_shoud_not_be_able_to_authenticate_an_user_with_non_existing_email(user_data, user_repository):
    authenticate_user_use_case_request = {
        "email": "john.doe@email.com",
        "password": user_data["password"],
    }

    with pytest.raises(ResourceNotFoundError) as err:
        AuthenticateUserUseCase(user_repository).execute(authenticate_user_use_case_request)
    assert str(err.value) == "Resource not found."


if __name__ == "__main__":
    pytest.main()
