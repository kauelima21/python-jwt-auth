import json
import logging
from src.services.tasks.use_cases.create_task import CreateTaskUseCase
from src.repositories.boto.boto_task_repository import BotoTaskRepository
from src.utils.errors.unauthorized import UnauthorizedError
from src.utils.event import authorize_user, json_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        user = authorize_user(event)

        if not event.get('body'):
            return None

        requestBody = json.loads(event.get('body'))

        logging.info(requestBody)

        task_repository = BotoTaskRepository()
        create_task_use_case = CreateTaskUseCase(task_repository)
        created_task = create_task_use_case.execute({
            "user_id": user.get("sub"),
            "title": requestBody["title"],
            "description": requestBody["description"],
        })

        logging.info(created_task)

        return json_response(None, 201)
    except UnauthorizedError as e:
        return json_response({
            "message": e.args[0]
        }, 401)
