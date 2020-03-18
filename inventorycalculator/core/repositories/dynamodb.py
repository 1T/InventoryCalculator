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
            raise DynamoDBError('Unable to put item')

    def get(self, key: str) -> Dict:
        try:
            resp = self._client.get_item(
                TableName=self._table_name,
                Key={'job_id': {'S': key}}
            )
            if 'Item' in resp:
                return {
                    'job_id': resp['Item']['job_id']['S'],
                    'status': resp['Item']['status']['S'],
                    'total_value': resp['Item']['total_value']['N']
                }
            raise DynamoDBError(f'Item not found by given key:{key}')
        except ClientError:
            raise DynamoDBError(f'Unable to get item by key:{key}')
