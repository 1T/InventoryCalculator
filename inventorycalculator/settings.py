from os import getenv

IS_PROD = getenv('ENV_TYPE', 'dev') == 'prod'
