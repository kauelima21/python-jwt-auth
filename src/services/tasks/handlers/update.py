import json
import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.utils.errors.resource_not_found import ResourceNotFoundError
from src.services.tasks.use_cases.update_task import UpdateTaskUseCase
from src.utils.errors.unauthorized import UnauthorizedError
from src.utils.event import authorize_user, json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        authorize_user(event)

        task_id = event["pathParameters"]["id"]

        if not event.get('body'):
            return None

        requestBody = json.loads(event.get('body'))

        task_repository = BotoTaskRepository()
        update_task_use_case = UpdateTaskUseCase(task_repository)
        task = update_task_use_case.execute({
            "id": task_id,
            "title": requestBody.get("title"),
            "description": requestBody.get("description"),
        })

        logging.info(task)

        return json_response(task.props)
    except UnauthorizedError as e:
        return json_response({
            "message": e.args[0]
        }, 401)
    except ResourceNotFoundError as e:
        return json_response({
            "message": e.args[0]
        }, 404)
