import boto3


dynamodb = boto3.resource(
  "dynamodb",
  region_name="us-east-1",
  endpoint_url="http://localhost:4566"
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
        BillingMode="PAY_PER_REQUEST"
    )

    print("Table status:", table.table_status)


if __name__ == "__main__":
    create_table()
