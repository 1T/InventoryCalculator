from logging import getLogger
from logging.config import dictConfig
from typing import Dict, Any
from json import dumps

from projectbase.settings import LOGGING_CONFIG


_logger = getLogger(__name__)
dictConfig(LOGGING_CONFIG)


def example_get(event: Dict[str, Any], _: Any) -> None:
    """Handle example get request."""
    # log dictionaries directly: adding key to root level override other fie
    _logger.info(f"Event: {dumps(event)}")
    # Or, log message and extra dictionary
    _logger.info("mymessage", extra={"userid": 1.23, "itemid": 0})
    return {
        'event': event
    }


def example_post(event: Dict[str, Any], _: Any) -> None:
    """Handle example get request."""
    _logger.info(f'handle post: {dumps(event)}')
    extra_dict = {
        'log': True,
        'most': True,
        'five': True,
        'keys': True
    }
    _logger.info(f'my_dict', extra=extra_dict)
    return {
        'event': event
    }
