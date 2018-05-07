from logging import getLogger, setLoggerClass
from logging.config import dictConfig
from typing import Dict, Any

from pythonjsonlogger.jsonlogger import OverrideKeyLogger

from projectbase.settings import LOGGING_CONFIG


setLoggerClass(OverrideKeyLogger)
_logger = getLogger(__name__)
dictConfig(LOGGING_CONFIG)


def example_get(event: Dict[str, Any], _: Any) -> None:
    """Handle example get request."""
    # log dictionaries directly: adding key to root level override other fie
    _logger.info(event)
    # Or, log message and extra dictionary
    _logger.info("mymessage", extra={"userid": 1.23, "itemid": 0})
    return {
        'event': event
    }


def example_post(event: Dict[str, Any], _: Any) -> None:
    """Handle example get request."""
    _logger.info('handle post', extra=event)
    return {
        'event': event
    }
