from OneTicketLogging import elasticsearch_logger

_logger = elasticsearch_logger(__name__)


class ProjectBaseError(Exception):
    def __init__(self, message, *args, **kwargs):
        _logger.exception(message)
        super().__init__(message, *args, **kwargs)


class ClientError(ProjectBaseError):
    def __init__(self, message, *args, **kwargs):
        super().__init__('Client error: ' + message, *args, **kwargs)


class ServiceError(ProjectBaseError):
    def __init__(self, message, *args, **kwargs):
        super().__init__('Service error: ' + message, *args, **kwargs)
