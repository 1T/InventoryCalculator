import pytest
from inventorycalculator.core.storages.s3_storage import S3Storage, boto3
from unittest.mock import patch, MagicMock, Mock
from inventorycalculator.errors import S3StorageError
from botocore.exceptions import ClientError

from tests.mocks import MockS3Body


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


@patch.object(boto3, 'client')
def test_get_success_call(mock_client):
    s3_client_mock = MagicMock()
    mock_client.return_value = s3_client_mock
    s3_client_mock.get_object.return_value = {
        'Body': MockS3Body(read=MagicMock(return_value=b'test_data'))
    }
    bucket_name = 'test_bucket'
    key = '0987654321'

    res = S3Storage(bucket_name).get(key)

    s3_client_mock.get_object.assert_called_with(
        Key=key,
        Bucket=bucket_name
    )
    mock_client.assert_called_with('s3')
    assert 'test_data' == res


@patch.object(boto3, 'client')
def test_get_failed(mock_client):
    with pytest.raises(S3StorageError):
        s3_client_mock = MagicMock()
        s3_client_mock.get_object = Mock(side_effect=ClientError({}, ''))
        mock_client.return_value = s3_client_mock
        bucket_name = 'test_bucket'
        key = '0987654321'

        storage = S3Storage(bucket_name)
        mock_client.assert_called_with('s3')

        storage.get(key)
