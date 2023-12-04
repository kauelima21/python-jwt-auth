import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.use_cases.delete_task import DeleteTaskUseCase
from src.utils.lambda_output import json_response


logger = logging.getLogger()


def lambda_handler(event, context):
    task_id = event["pathParameters"]["id"]
    task_repository = BotoTaskRepository()
    delete_task_use_case = DeleteTaskUseCase(task_repository)
    task = delete_task_use_case.execute(task_id)

    logging.info(task)

    return json_response(task)
