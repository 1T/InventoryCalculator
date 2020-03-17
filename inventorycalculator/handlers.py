from typing import Dict, Any
from uuid import uuid4
from inventorycalculator.core.loaders.file_loader import FileLoader
from inventorycalculator.core.repositories.dynamodb import DynamoDBTable
from inventorycalculator.core.storages.s3_storage import S3Storage
from inventorycalculator.core.workers.aws_lambda import AwsLambda
from inventorycalculator.settings import S3_BUCKET, TABLE_NAME, STATUSES, ASYNC_WORKER

# from OneTicketLogging import elasticsearch_logger


# _logger = elasticsearch_logger(__name__)

file_loader = FileLoader()
storage = S3Storage(S3_BUCKET)
db_table = DynamoDBTable(TABLE_NAME)
async_worker = AwsLambda(ASYNC_WORKER)


def create_inventory_calculator_job(event: Dict[str, Any], _: Any) -> Dict:
    """Creates inventory calculator job for async processing"""
    file_content = file_loader.by_url(event['body']['url'])
    job_id = str(uuid4())
    job = {'job_id': job_id}
    storage.upload(job_id, file_content)
    db_table.put({
        **job,
        'status': STATUSES.RUNNING,
        'total_value': None
    })
    async_worker.async_invoke(job)
    return job


def example_post(event: Dict[str, Any], _: Any) -> Dict:
    """Handle example post request."""
    # _logger.info(event)
    return {
        'event': event
    }
