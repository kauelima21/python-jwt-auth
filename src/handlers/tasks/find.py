import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.use_cases.errors.resource_not_found import ResourceNotFoundError
from src.use_cases.find_task import FindTaskUseCase
from src.utils.lambda_output import json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    task_id = event["pathParameters"]["id"]
    task_repository = BotoTaskRepository()
    find_task_use_case = FindTaskUseCase(task_repository)
    try:
        task = find_task_use_case.execute(task_id)
    except ResourceNotFoundError:
        return json_response({
            "message": "Task não encontrada."
        }, 404)

    logging.info(task)

    return json_response(task)
