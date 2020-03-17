from os import getenv

IS_PROD = getenv('ENV_TYPE', 'dev') == 'prod'
S3_BUCKET = getenv('S3_BUCKET', 'vd-inventory-calculator')
TABLE_NAME = getenv('TABLE_NAME', 'vd-inventory-calculator')
ASYNC_WORKER = getenv('ASYNC_WORKER', 'vd-async-worker')


class STATUSES:
    RUNNING = 'RUNNING'
    FAILED = 'FAILED'
    SUCCEEDED = 'SUCCEEDED'
