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
        'total_value': 0
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
            'total_value': 0
        }

        table = DynamoDBTable(table_name)
        mock_client.assert_called_with('dynamodb')

        table.put(fake_payload)


@patch.object(boto3, 'client')
def test_get_find_item(mock_client):
    dynamo_client_mock = MagicMock()
    mock_client.return_value = dynamo_client_mock
    table_name = 'test_table'
    dynamo_client_mock.get_item.return_value = {
        'Item': {
            'job_id': {
                'S': '0987654321',
            },
            'status': {
                'S': STATUSES.RUNNING,
            },
            'total_value': {
                'N': 0,
            },
        }
    }

    res = DynamoDBTable(table_name).get('0987654321')

    dynamo_client_mock.get_item.assert_called_with(
        TableName=table_name,
        Key={'job_id': {'S': '0987654321'}}
    )
    mock_client.assert_called_with('dynamodb')
    assert {
        'job_id': '0987654321',
        'status': STATUSES.RUNNING,
        'total_value': 0
    } == res


@patch.object(boto3, 'client')
def test_get_item_not_exist(mock_client):
    with pytest.raises(DynamoDBError):
        dynamo_client_mock = MagicMock()
        mock_client.return_value = dynamo_client_mock
        table_name = 'test_table'
        dynamo_client_mock.get_item.return_value = {}

        DynamoDBTable(table_name).get('0987654321')

    dynamo_client_mock.get_item.assert_called_with(
        TableName=table_name,
        Key={'job_id': {'S': '0987654321'}}
    )
    mock_client.assert_called_with('dynamodb')


@patch.object(boto3, 'client')
def test_get_failed_call(mock_client):
    with pytest.raises(DynamoDBError):
        dynamo_client_mock = MagicMock()
        dynamo_client_mock.get_item = Mock(side_effect=ClientError({}, ''))
        mock_client.return_value = dynamo_client_mock
        table_name = 'test_table'

        table = DynamoDBTable(table_name)
        mock_client.assert_called_with('dynamodb')

        table.get('0987654321')
