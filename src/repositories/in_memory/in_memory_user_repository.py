from datetime import datetime
from src.entities.user import User
from src.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._data = []

    def findById(self, id: str) -> User:
        filtered_user = filter(lambda user: user.get("id") == id, self._data)
        user_array = list(filtered_user)
        if len(user_array) <= 0:
          return None

        return User(user_array[0], user_array[0]["id"])
    
    def findByEmail(self, email: str) -> User:
        filtered_user = filter(lambda user: user.get("email") == email, self._data)
        user_array = list(filtered_user)
        if len(user_array) <= 0:
          return None

        return User(user_array[0], user_array[0]["id"])

    def findByUsername(self, username: str) -> User:
        filtered_user = filter(lambda user: user.get("username") == username, self._data)
        user_array = list(filtered_user)
        if len(user_array) <= 0:
          return None

        return User(user_array[0], user_array[0]["id"])

    def validate(self, user: User) -> User:
        index = 0
        user_to_validate = None

        for i, item in enumerate(self._data):
          if item.get("id") == user.get("id"):
            index = i
            user_to_validate = item

        user_to_validate["validated_at"] = datetime.now()
        user_to_validate["updated_at"] = datetime.now()

        self._data[index] = user_to_validate
        return User(user_to_validate, user_to_validate["id"])

    def save(self, user: User) -> User:
        self._data.append(user)
        return user
