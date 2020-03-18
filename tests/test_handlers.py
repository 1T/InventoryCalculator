from unittest.mock import patch, ANY, call
from inventorycalculator.core.loaders.file_loader import FileLoader
from inventorycalculator.core.parsers.inventory_parser import InventoryParser
from inventorycalculator.core.storages.s3_storage import S3Storage
from inventorycalculator.core.repositories.dynamodb import DynamoDBTable
from inventorycalculator.core.workers.aws_lambda import AwsLambda
from inventorycalculator.handlers import crawl_job_handler, async_worker_handler, status_check_handler
from inventorycalculator.models.inventory_item import InventoryItem
from inventorycalculator.settings import STATUSES


@patch.object(FileLoader, 'by_url')
@patch.object(S3Storage, 'upload')
@patch.object(DynamoDBTable, 'put')
@patch.object(AwsLambda, 'async_invoke')
def test_crawl_job_handler(mock_async_invoke, mock_table_put, mock_s3_upload, mock_file_loader):
    mock_file_loader.return_value = 'file content'
    event = {'url': 'test_url'}

    res = crawl_job_handler(event, None)

    mock_file_loader.assert_called_with('test_url')
    mock_s3_upload.assert_has_calls([
        call(ANY, 'file content')
    ])
    mock_table_put.assert_has_calls([
        call({
            'job_id': ANY,
            'status': STATUSES.RUNNING,
            'total_value': 0
        })
    ])
    mock_async_invoke.assert_called_with({'job_id': ANY})
    assert {'job_id': ANY} == res


@patch.object(S3Storage, 'get')
@patch.object(DynamoDBTable, 'put')
@patch.object(DynamoDBTable, 'get')
@patch.object(InventoryParser, 'from_tsv')
def test_async_worker_handler(mock_from_tsv, mock_table_get, mock_table_put, mock_s3_get):
    event = {'job_id': '0987654321'}
    mock_s3_get.return_value = 'raw file'
    mock_from_tsv.return_value = [
        InventoryItem(quantity=1, cost=15.5),
        InventoryItem(quantity=2, cost=5.5),
        InventoryItem(quantity=3, cost=1.5)
    ]

    res = async_worker_handler(event, None)

    mock_s3_get.assert_called_with('0987654321')
    mock_from_tsv.assert_called_with('raw file')
    mock_table_get.assert_called_with('0987654321')
    mock_table_put.assert_called_with({
        'job_id': '0987654321',
        'status': STATUSES.SUCCEEDED,
        'total_value': 31.0
    })
    assert {'job_id': '0987654321'} == res


@patch.object(DynamoDBTable, 'get')
def test_status_check_handler(mock_table_get):
    event = {'job_id': '0987654321'}
    mock_table_get.return_value = {
        'job_id': '0987654321',
        'status': STATUSES.SUCCEEDED,
        'total_value': 10.0
    }

    res = status_check_handler(event, None)

    mock_table_get.assert_called_with('0987654321')
    assert {
               'status': STATUSES.SUCCEEDED,
               'total_value': 10.0
           } == res
