import pytest
from inventorycalculator.core.storages.s3_storage import S3Storage, boto3
from unittest.mock import patch, MagicMock, Mock
from inventorycalculator.errors import S3StorageError
from botocore.exceptions import ClientError


@patch.object(boto3, 'client')
def test_upload_success_call(mock_client):
    s3_client_mock = MagicMock()
    mock_client.return_value = s3_client_mock
    bucket_name = 'test_bucket'
    fake_data = 'test_data'
    key = '0987654321'

    S3Storage(bucket_name).upload(key, fake_data)

    s3_client_mock.put_object.assert_called_with(
        Body=fake_data.encode(),
        Key=key,
        Bucket=bucket_name
    )
    mock_client.assert_called_with('s3')


@patch.object(boto3, 'client')
def test_upload_failed(mock_client):
    with pytest.raises(S3StorageError):
        s3_client_mock = MagicMock()
        s3_client_mock.put_object = Mock(side_effect=ClientError({}, ''))
        mock_client.return_value = s3_client_mock
        bucket_name = 'test_bucket'
        fake_data = 'test_data'
        key = '0987654321'

        storage = S3Storage(bucket_name)
        mock_client.assert_called_with('s3')

        storage.upload(key, fake_data)
