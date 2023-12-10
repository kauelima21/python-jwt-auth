import pytest
from src.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository
from src.services.tasks.use_cases.fetch_tasks import FetchTasksUseCase


@pytest.fixture()
def task_repository():
    task_repository = InMemoryTaskRepository()
    task_repository.save({
        "title": "My Task 01",
        "description": "This is my first task.",
    })
    task_repository.save({
        "title": "My Task 02",
        "description": "This is my second task.",
    })
    yield task_repository


def test_it_shoud_be_able_to_fetch_all_tasks(task_repository):
    tasks = FetchTasksUseCase(task_repository).execute()
    tasks_length = len(tasks)

    assert tasks_length == 2
    assert tasks[0].get("title") == "My Task 01"


if __name__ == "__main__":
    pytest.main()
