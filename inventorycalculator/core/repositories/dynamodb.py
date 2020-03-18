import boto3
from botocore.exceptions import ClientError
from inventorycalculator.errors import DynamoDBError
from typing import Dict


class DynamoDBTable:

    _ATTS = ('job_id', 'status', 'total_value')
    _DATA_TYPES = {
        str: 'S',
        float: 'N',
        int: 'N'
    }

    def __init__(self, table_name: str):
        self._table_name = table_name
        self._client = boto3.client('dynamodb')

    def put(self, item: Dict):
        try:
            prepared_item = {
                attr_name: self._prepare_attr(item[attr_name])
                for attr_name in self._ATTS
            }
            self._client.put_item(
                TableName=self._table_name,
                Item=prepared_item
            )
        except ClientError:
            raise DynamoDBError('Unable to put item')

    def _prepare_attr(self, attr_value) -> Dict:
        return {
            self._DATA_TYPES[type(attr_value)]: str(attr_value)
        }

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
