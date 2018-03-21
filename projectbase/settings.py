from logging import INFO, ERROR
from os import getenv

PROD = getenv('EnvType', 'dev') == 'prod'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'venues': {
            'level': INFO,
        },
        'boto3': {
            'level': ERROR,
        },
        'botocore': {
            'level': ERROR,
        },
    },
}
