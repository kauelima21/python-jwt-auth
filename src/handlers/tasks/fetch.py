import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.use_cases.fetch_tasks import FetchTasksUseCase
from src.utils.lambda_output import json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    task_repository = BotoTaskRepository()
    fetch_tasks_use_case = FetchTasksUseCase(task_repository)
    tasks = fetch_tasks_use_case.execute()

    logging.info(tasks)

    return json_response(tasks)
