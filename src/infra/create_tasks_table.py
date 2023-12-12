import boto3

dynamodb = boto3.resource(
  "dynamodb",
  region_name="sa-east-1"
)


def create_table():
    table = dynamodb.create_table(
        TableName="tasks",
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            }
        ],
         GlobalSecondaryIndexes=[{
            "IndexName": "user_id-index",
            "KeySchema": [
                {
                    "AttributeName": "user_id",
                    "KeyType": "HASH"
                }
            ],
            "Projection": {
                "ProjectionType": "ALL"
            }
        }],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Table status:", table.table_status)


if __name__ == "__main__":
    create_table()
