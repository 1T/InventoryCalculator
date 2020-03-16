from typing import Dict, Any

from OneTicketLogging import elasticsearch_logger


_logger = elasticsearch_logger(__name__)


def example_get(event: Dict[str, Any], _: Any) -> Dict:
    """Handle example get request."""
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
