from logging import Filter, LoggerAdapter, StreamHandler, INFO, getLogger
from logging.config import dictConfig
from uuid import uuid4

from projectbase.settings import LOGGING_CONFIG, USER_ID, JOB_ID, AWS_BATCH_JOB_ID


class JobIdFilter(Filter):
    # Override to use custom JobID (not AWS_BATCH_JOB_ID)
    def filter(self, record):
        jobid = ':'.join([JOB_ID, AWS_BATCH_JOB_ID]) \
            if AWS_BATCH_JOB_ID else JOB_ID
        record.jobid = jobid
        return True


class BatchAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        extra = {**kwargs.get('extra', {}), **self.extra}
        return (msg, {'extra': extra})


class NoLambdaLoggerFilter(Filter):
    def __init__(self):
        Filter.__init__(self)
        self.request_id = str(uuid4())

    def filter(self, record):
        record.aws_request_id = self.request_id
        return True


class NoLambdaLoggerHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
        self.setLevel(INFO)


def init_logging():
    import __main__
    if not hasattr(__main__, 'LambdaLoggerFilter'):
        __main__.LambdaLoggerFilter = NoLambdaLoggerFilter
    if not hasattr(__main__, 'LambdaLoggerHandler'):
        __main__.LambdaLoggerHandler = NoLambdaLoggerHandler
    dictConfig(LOGGING_CONFIG)


def get_logger():
    ids = [JOB_ID, AWS_BATCH_JOB_ID]
    jobid = ':'.join(ids) if AWS_BATCH_JOB_ID else JOB_ID
    extra = {'userid': USER_ID, 'jobid': jobid} if USER_ID else {}
    return BatchAdapter(getLogger(__name__), extra=extra)