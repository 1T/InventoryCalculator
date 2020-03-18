import boto3
from botocore.exceptions import ClientError
from inventorycalculator.errors import S3StorageError
from OneTicketLogging import elasticsearch_logger


_logger = elasticsearch_logger(__name__)


class S3Storage:
    def __init__(self, bucket_name: str):
        self._bucket_name = bucket_name
        self._client = boto3.client('s3')

    def upload(self, key: str, data: str):
        try:
            self._client.put_object(
                Body=data.encode(),
                Key=key,
                Bucket=self._bucket_name
            )
        except ClientError as e:
            _logger.error(e)
            raise S3StorageError('Unable to upload given data')

    def get(self, key: str) -> str:
        try:
            return self._client.get_object(
                Key=key,
                Bucket=self._bucket_name
            )['Body'].read().decode('utf-8')
        except ClientError as e:
            _logger.error(e)
            raise S3StorageError(f'Resource not exists by given key:{key}')
