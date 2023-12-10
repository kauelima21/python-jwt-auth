import pytest
from src.repositories.in_memory.in_memory_task_repository import InMemoryTaskRepository
from src.services.tasks.use_cases.delete_task import DeleteTaskUseCase
from src.utils.errors.resource_not_found import ResourceNotFoundError


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


def test_it_shoud_be_able_to_delete_a_task(task_repository):
    task_id = "id-2"
    task = DeleteTaskUseCase(task_repository).execute(task_id)
    tasks = task_repository.findAll()

    assert task.get("title") == "My Task 02"
    assert len(tasks) == 1


def test_it_shoud_not_be_able_to_delete_a_task_that_not_exists(task_repository):
    task_id = "id-5"

    with pytest.raises(ResourceNotFoundError) as err:
        DeleteTaskUseCase(task_repository).execute(task_id)
    assert str(err.value) == "Resource Not Found"


if __name__ == "__main__":
    pytest.main()
