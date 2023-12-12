import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.utils.errors.resource_not_found import ResourceNotFoundError
from src.services.tasks.use_cases.find_task import FindTaskUseCase
from src.utils.errors.unauthorized import UnauthorizedError
from src.utils.event import authorize_user, json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        authorize_user(event)

        task_id = event["pathParameters"]["id"]

        task_repository = BotoTaskRepository()
        find_task_use_case = FindTaskUseCase(task_repository)
        task = find_task_use_case.execute(task_id)

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
