import boto3
from json import dumps
from typing import Dict
from botocore.exceptions import ClientError
from inventorycalculator.errors import InvokeLambdaError
from OneTicketLogging import elasticsearch_logger


_logger = elasticsearch_logger(__name__)


class AwsLambda:
    def __init__(self, name: str, **kwargs):
        self._name = name
        self._client = boto3.client('lambda')
        self._invocation_type = kwargs.get('InvocationType', 'Event')

    def async_invoke(self, payload: Dict):
        try:
            self._client.invoke(
                FunctionName=self._name,
                Payload=dumps(payload),
                InvocationType=self._invocation_type
            )
        except ClientError as exc:
            _logger.error(exc)
            raise InvokeLambdaError(f'{self._name} invocation failed: {exc}')
