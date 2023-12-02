import pytest
from src.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository
from src.use_cases.find_task import FindTaskUseCase


@pytest.fixture()
def task_repository():
    task_repository = InMemoryTaskRepository()
    task_repository.save({
        "id": "id-1",
        "title": "My Task 01",
        "description": "This is my first task.",
    })
    task_repository.save({
        "id": "id-2",
        "title": "My Task 02",
        "description": "This is my second task.",
    })
    yield task_repository


def test_it_shoud_be_able_to_fetch_all_tasks(task_repository):
    task_id = "id-2"
    task = FindTaskUseCase(task_repository).execute(task_id)

    assert task.get("title") == "My Task 02"


if __name__ == "__main__":
    pytest.main()

