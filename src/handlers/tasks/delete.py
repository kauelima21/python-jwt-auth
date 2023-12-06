import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.use_cases.delete_task import DeleteTaskUseCase
from src.use_cases.errors.resource_not_found import ResourceNotFoundError
from src.utils.lambda_output import json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    task_id = event["pathParameters"]["id"]
    task_repository = BotoTaskRepository()
    delete_task_use_case = DeleteTaskUseCase(task_repository)

    try:
        task = delete_task_use_case.execute(task_id)
    except ResourceNotFoundError:
        return json_response({
            "message": "Task não encontrada."
        }, 404)

    logging.info(task)

    return json_response({
        "message": "Task {} deleted".format(task_id)
    })
