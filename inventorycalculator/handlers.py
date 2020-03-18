from typing import Dict, Any
from uuid import uuid4
from inventorycalculator.core.loaders.file_loader import FileLoader
from inventorycalculator.core.parsers.inventory_parser import InventoryParser
from inventorycalculator.core.repositories.dynamodb import DynamoDBTable
from inventorycalculator.core.storages.s3_storage import S3Storage
from inventorycalculator.core.workers.aws_lambda import AwsLambda
from inventorycalculator.errors import S3StorageError, DynamoDBError, AsyncWorkerError, InvalidInventoryDataFormatError
from inventorycalculator.settings import S3_BUCKET, TABLE_NAME, STATUSES, ASYNC_WORKER
from OneTicketLogging import elasticsearch_logger


_logger = elasticsearch_logger(__name__)
file_loader = FileLoader()
storage = S3Storage(S3_BUCKET)
db_table = DynamoDBTable(TABLE_NAME)
async_worker = AwsLambda(ASYNC_WORKER)
inventory_parser = InventoryParser()


def crawl_job_handler(event: Dict[str, Any], _: Any) -> Dict:
    """Creates inventory calculator job for async processing"""
    _logger.info(event)
    file_content = file_loader.by_url(event['url'])
    job_id = str(uuid4())
    job = {'job_id': job_id}
    storage.upload(job_id, file_content)
    async_worker.async_invoke(job)
    db_table.put({
        **job,
        'status': STATUSES.RUNNING,
        'total_value': 0
    })
    return job


def async_worker_handler(event: Dict[str, Any], _: Any):
    """Process the tickets"""
    _logger.info(event)
    job_id = event.get('job_id')
    try:
        db_table.get(job_id)
        tickets = inventory_parser.from_tsv(storage.get(job_id))
        total_value = sum([ticket.value for ticket in tickets])
        db_table.put({
            'job_id': job_id,
            'status': STATUSES.SUCCEEDED,
            'total_value': total_value
        })
    except (S3StorageError, DynamoDBError, InvalidInventoryDataFormatError) as e:
        _logger.error(e)
        db_table.put({
            'job_id': job_id,
            'status': STATUSES.FAILED
        })
        raise AsyncWorkerError(f'Unable to proceed job with "job_id":{job_id}')


def status_check_handler(event: Dict[str, Any], _: Any) -> Dict:
    """Check the status of tickets processing"""
    _logger.info(event)
    payload = db_table.get(event['job_id'])
    return {
        'status': payload['status'],
        'total_value': payload['total_value']
    }
