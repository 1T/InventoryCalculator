import pytest
from inventorycalculator.core.repositories.dynamodb import DynamoDBTable, boto3
from unittest.mock import patch, MagicMock, Mock
from inventorycalculator.errors import DynamoDBError
from botocore.exceptions import ClientError
from inventorycalculator.settings import STATUSES


@patch.object(boto3, 'client')
def test_put_success_call(mock_client):
    dynamo_client_mock = MagicMock()
    mock_client.return_value = dynamo_client_mock
    table_name = 'test_table'
    fake_payload = {
        'job_id': '0987654321',
        'status': STATUSES.RUNNING,
        'total_value': None
    }

    DynamoDBTable(table_name).put(fake_payload)

    dynamo_client_mock.put_item.assert_called_with(
        TableName=table_name,
        Item=fake_payload
    )
    mock_client.assert_called_with('dynamodb')


@patch.object(boto3, 'client')
def test_put_failed_call(mock_client):
    with pytest.raises(DynamoDBError):
        dynamo_client_mock = MagicMock()
        dynamo_client_mock.put_item = Mock(side_effect=ClientError({}, ''))
        mock_client.return_value = dynamo_client_mock
        table_name = 'test_table'
        fake_payload = {
            'job_id': '0987654321',
            'status': STATUSES.RUNNING,
            'total_value': None
        }

        table = DynamoDBTable(table_name)
        mock_client.assert_called_with('dynamodb')

        table.put(fake_payload)
