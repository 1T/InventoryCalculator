import boto3
from botocore.exceptions import ClientError
from inventorycalculator.errors import DynamoDBError
from typing import Dict


class DynamoDBTable:
    def __init__(self, table_name: str):
        self._table_name = table_name
        self._client = boto3.client('dynamodb')

    def put(self, item: Dict):
        try:
            self._client.put_item(
                TableName=self._table_name,
                Item=item
            )
        except ClientError:
            raise DynamoDBError('Unable to put item into')

    def get(self, key):
        pass
