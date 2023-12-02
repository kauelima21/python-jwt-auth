import pytest
from src.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository
from src.use_cases.create_task import CreateTaskUseCase


@pytest.fixture()
def task_data():
    task_data = {
        "title": "My Task",
        "description": "This is my task.",
    }
    yield task_data


def test_it_shoud_be_able_to_create_a_task(task_data):
    task_repository = InMemoryTaskRepository()
    create_task_use_case = CreateTaskUseCase(task_repository)
    created_task = create_task_use_case.execute({
        "title": task_data["title"],
        "description": task_data["description"]
    })

    assert created_task.title == task_data["title"]
    assert created_task.description == task_data["description"]


if __name__ == "__main__":
    pytest.main()
