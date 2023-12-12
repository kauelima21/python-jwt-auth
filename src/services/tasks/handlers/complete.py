import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.services.tasks.use_cases.complete_task import CompleteTaskUseCase
from src.utils.errors.resource_not_found import ResourceNotFoundError
from src.utils.event import authorize_user, json_response
from src.utils.errors.unauthorized import UnauthorizedError


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        authorize_user(event)

        task_id = event["pathParameters"]["id"]
        task_repository = BotoTaskRepository()
        complete_task_use_case = CompleteTaskUseCase(task_repository)

        task = complete_task_use_case.execute(task_id)

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
