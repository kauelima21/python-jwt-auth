import json
from src.use_cases.create_task import CreateTaskUseCase
from src.repositories.boto.boto_task_repository import BotoTaskRepository


def lambda_handler(event, context):
  if not event.get('body'):
    return None

  requestBody = json.loads(event.get('body'))

  task_repository = BotoTaskRepository()
  create_task_use_case = CreateTaskUseCase(task_repository)
  create_task_use_case.execute({
      "title": requestBody["title"],
      "description": requestBody["description"]
  })

  return {
      "statusCode": 201,
      "body": json.dumps(None),
      "headers": {
          "Content-Type": "application/json"
      }
  }
