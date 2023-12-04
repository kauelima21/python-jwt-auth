import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.use_cases.find_task import FindTaskUseCase
from src.utils.lambda_output import json_response


logger = logging.getLogger()


def lambda_handler(event, context):
    task_id = event["pathParameters"]["id"]
    task_repository = BotoTaskRepository()
    find_task_use_case = FindTaskUseCase(task_repository)
    task = find_task_use_case.execute(task_id)

    logging.info(task)

    return json_response(task)
