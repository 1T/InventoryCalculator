from logging import Filter
from os import getenv

APP_NAME = 'projectbase'

PROD = getenv('EnvType', 'dev') == 'prod'


class AppNameFilter(Filter):
    def filter(self, record):
        record.app_name = APP_NAME
        return True


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logstream': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt':
                '[%(levelname)s]\t%(asctime)s.%(msecs)dZ'
                '\t%(aws_request_id)s\t%(message)s\t%(app_name)s\n',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
        }
    },
    'filters': {
        'requestid': {
            '()': '__main__.LambdaLoggerFilter',
        },
        'appname': {
            '()': 'loggingtest.settings.AppNameFilter',
        }
    },
    'handlers': {
        'logstreamer': {
            'class': '__main__.LambdaLoggerHandler',
            'filters': ['requestid', 'appname'],
            'formatter': 'logstream',
            'level': 'INFO',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['logstreamer']
        },
        APP_NAME: {
            'level': 'INFO',
            'handlers': ['logstreamer'],
            # required to avoid double logging with root logger
            'propagate': False
        },
        'boto3': {
            'level': 'ERROR'
        },
        'botocore': {
            'level': 'ERROR'
        }
    },
}
