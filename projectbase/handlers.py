from logging import getLogger
from logging.config import dictConfig
from typing import Dict, Any

from kinesislogger import LOGGING_CONFIG


_logger = getLogger(__name__)
dictConfig(LOGGING_CONFIG)


def example_get(event: Dict[str, Any], _: Any) -> Dict:
    """Handle example get request."""
    for i in range(100):
        _logger.info(event)
    return {
        'event': event
    }


def example_post(event: Dict[str, Any], _: Any) -> Dict:
    """Handle example post request."""
    _logger.info(event)
    return {
        'event': event
    }
