import uuid
from typing import TypedDict, Optional


class TaskProps(TypedDict):
    id: Optional[str]
    title: str
    description: str
    completed_at: Optional[str]
    user_id: str
    created_at: str
    updated_at: str


class Task:
    def __init__(self, props: TaskProps, id: str = None) -> None:
        self.props = self._prepare_props(props)
        self._id = id if id else uuid.uuid4()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self.props.get("title")

    @title.setter
    def title(self, title):
        self.props["title"] = title

    @property
    def description(self):
        return self.props.get("description")

    @description.setter
    def description(self, description):
        self.props["description"] = description

    @property
    def completed_at(self):
        return self.props.get("completed_at")

    @property
    def user_id(self):
        return self.props.get("user_id")

    @property
    def created_at(self):
        return self.props.get("created_at")

    @property
    def updated_at(self):
        return self.props.get("updated_at")

    def _prepare_props(self, props: TaskProps):
        prepared_props = {
            "title": props.get("title"),
            "description": props.get("description"),
            "user_id": props.get("user_id"),
            "created_at": props.get("created_at"),
            "updated_at": props.get("updated_at"),
        }

        if props.get("completed_at"):
            prepared_props["completed_at"] = props.get("completed_at")

        if props.get("id"):
            prepared_props["id"] = props.get("id")

        return prepared_props
