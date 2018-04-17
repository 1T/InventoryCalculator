from logging import INFO, ERROR
from os import getenv


CLIENT_ID = getenv('CLIENT_ID', '')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'ssmtest': {
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
