# from OneTicketLogging import elasticsearch_logger

# _logger = elasticsearch_logger(__name__)


class InventoryCalculatorBaseError(Exception):
    def __init__(self, message, *args, **kwargs):
        # _logger.exception(message)
        super().__init__(message, *args, **kwargs)


class LoadFileError(InventoryCalculatorBaseError):
    pass


class InvalidInventoryDataFormatError(InventoryCalculatorBaseError):
    pass


class InvokeLambdaError(InventoryCalculatorBaseError):
    pass


class AsyncWorkerError(InventoryCalculatorBaseError):
    pass


class S3StorageError(InventoryCalculatorBaseError):
    pass


class DynamoDBError(InventoryCalculatorBaseError):
    pass
