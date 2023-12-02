import uuid
from typing import TypedDict, Optional


class TaskProps(TypedDict):
  id: Optional[str]
  title: str
  description: str
  completed_at: Optional[str]
  created_at: str
  updated_at: str


class Task:
  def __init__(self, props: TaskProps, id: str = None) -> None:
    self.props = props
    self._id = id if id else uuid.uuid4()

  @property
  def id(self):
    return self._id

  @property
  def title(self):
    return self.props.get("title")

  @property
  def description(self):
    return self.props.get("description")

  @property
  def completed_at(self):
    return self.props.get("completed_at")

  @property
  def created_at(self):
    return self.props.get("created_at")

  @property
  def updated_at(self):
    return self.props.get("updated_at")
