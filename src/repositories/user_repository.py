from abc import ABC, abstractmethod
from src.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def findById(self, id: str) -> User:
        pass

    @abstractmethod
    def findByEmail(self, email: str) -> User:
        pass

    @abstractmethod
    def findByUsername(self, username: str) -> User:
        pass

    @abstractmethod
    def validate(self, user: User) -> User:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass
