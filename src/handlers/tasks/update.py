import json
import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.use_cases.errors.resource_not_found import ResourceNotFoundError
from src.use_cases.update_task import UpdateTaskUseCase
from src.utils.lambda_output import json_response


logger = logging.getLogger()


def lambda_handler(event, context):
    task_id = event["pathParameters"]["id"]

    if not event.get('body'):
        return None

    requestBody = json.loads(event.get('body'))
    task_repository = BotoTaskRepository()
    update_task_use_case = UpdateTaskUseCase(task_repository)

    try:
        task = update_task_use_case.execute({
        "id": task_id,
        "title": requestBody.get("title"),
        "description": requestBody.get("description"),
    })
    except ResourceNotFoundError:
        return json_response({
            "message": "Task não encontrada."
        }, 404)

    logging.info(task)

    return json_response(task)
