import boto3
from botocore.exceptions import ClientError
from inventorycalculator.errors import S3StorageError


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
        except ClientError:
            raise S3StorageError('Unable to upload given data')