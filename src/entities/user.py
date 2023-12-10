import uuid
from typing import TypedDict, Optional


class UserProps(TypedDict):
    id: Optional[str]
    username: str
    email: str
    password_hash: str
    validated_at: Optional[str]
    created_at: str
    updated_at: str


class User:
    def __init__(self, props: UserProps, id: str = None) -> None:
        self.props = props
        self._id = id if id else uuid.uuid4()

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self.props.get("username")

    @property
    def email(self):
        return self.props.get("email")

    @property
    def password_hash(self):
        return self.props.get("password_hash")

    @property
    def validated_at(self):
        return self.props.get("validated_at")

    @property
    def created_at(self):
        return self.props.get("created_at")

    @property
    def updated_at(self):
        return self.props.get("updated_at")
