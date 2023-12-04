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
                "KeyType": "HASH"  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Table status:", table.table_status)


if __name__ == "__main__":
    create_table()
