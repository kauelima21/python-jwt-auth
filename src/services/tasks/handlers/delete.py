import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.services.tasks.use_cases.delete_task import DeleteTaskUseCase
from src.utils.errors.resource_not_found import ResourceNotFoundError
from src.utils.errors.unauthorized import UnauthorizedError
from src.utils.event import authorize_user, json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        authorize_user(event)

        task_id = event["pathParameters"]["id"]
        task_repository = BotoTaskRepository()
        delete_task_use_case = DeleteTaskUseCase(task_repository)

        task = delete_task_use_case.execute(task_id)

        logging.info(task)

        return json_response("Task {} deleted".format(task_id))
    except UnauthorizedError as e:
        return json_response({
            "message": e.args[0]
        }, 401)
    except ResourceNotFoundError as e:
        return json_response({
            "message": e.args[0]
        }, 404)
