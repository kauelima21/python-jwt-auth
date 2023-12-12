import logging
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.services.tasks.use_cases.fetch_tasks import FetchTasksUseCase
from src.utils.errors.unauthorized import UnauthorizedError
from src.utils.event import authorize_user, json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        user = authorize_user(event)

        task_repository = BotoTaskRepository()
        fetch_tasks_use_case = FetchTasksUseCase(task_repository)
        tasks = fetch_tasks_use_case.execute(user.get("sub"))

        logging.info(tasks)

        return json_response(tasks)
    except UnauthorizedError as e:
        return json_response({
            "message": e.args[0]
        }, 401)
