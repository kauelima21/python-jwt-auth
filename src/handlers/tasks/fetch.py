import json
from src.use_cases.create_task import CreateTaskUseCase
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.use_cases.fetch_tasks import FetchTasksUseCase


def lambda_handler(event, context):
    task_repository = BotoTaskRepository()
    fetch_tasks_use_case = FetchTasksUseCase(task_repository)
    tasks = fetch_tasks_use_case.execute()

    return {
        "statusCode": 200,
        "body": json.dumps(tasks),
        "headers": {
            "Content-Type": "application/json"
        }
    }
