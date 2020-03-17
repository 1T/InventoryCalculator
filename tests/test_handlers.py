from unittest.mock import patch, ANY, call
from inventorycalculator.core.loaders.file_loader import FileLoader
from inventorycalculator.core.storages.s3_storage import S3Storage
from inventorycalculator.core.repositories.dynamodb import DynamoDBTable
from inventorycalculator.core.workers.aws_lambda import AwsLambda
from inventorycalculator.handlers import create_inventory_calculator_job
from inventorycalculator.settings import STATUSES


@patch.object(FileLoader, 'by_url')
@patch.object(S3Storage, 'upload')
@patch.object(DynamoDBTable, 'put')
@patch.object(AwsLambda, 'async_invoke')
def test_create_inventory_calculator_job(mock_async_invoke, mock_table_put, mock_s3_upload, mock_file_loader):
    mock_file_loader.return_value = 'file content'
    event = {
        'body': {
            'url': 'test_url'
        }
    }

    res = create_inventory_calculator_job(event, None)

    mock_file_loader.assert_called_with('test_url')
    mock_s3_upload.assert_has_calls([
        call(ANY, 'file content')
    ])
    mock_table_put.assert_has_calls([
        call({
            'job_id': ANY,
            'status': STATUSES.RUNNING,
            'total_value': None
        })
    ])
    mock_async_invoke.assert_called_with({'job_id': ANY})
    assert {'job_id': ANY} == res
