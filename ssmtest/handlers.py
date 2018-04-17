from logging import getLogger
from logging.config import dictConfig
from typing import Dict, Any

from ssmtest.settings import LOGGING_CONFIG, CLIENT_ID

_logger = getLogger(__name__)
dictConfig(LOGGING_CONFIG)


def example_get(event: Dict[str, Any], _: Any) -> None:
    """Handle example get request."""
    _logger.info(f'Got event: {event}')
    return {
        'event': event
    }


def example_post(event: Dict[str, Any], _: Any) -> None:
    """Handle example get request."""
    _logger.info(f'Got event: {event}')
    return {
        'event': event
    }
