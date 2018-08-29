from typing import Dict, Any

from kinesislogger import get_logger


_logger = get_logger()


def example_get(event: Dict[str, Any], _: Any) -> Dict:
    """Handle example get request."""
    for i in range(100):
        _logger.info(event, extra={'userid': 'lolol'})
    return {
        'event': event
    }


def example_post(event: Dict[str, Any], _: Any) -> Dict:
    """Handle example post request."""
    _logger.info(event)
    return {
        'event': event
    }
