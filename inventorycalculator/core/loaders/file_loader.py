import requests
from inventorycalculator.errors import LoadFileError
from OneTicketLogging import elasticsearch_logger


_logger = elasticsearch_logger(__name__)


class FileLoader:

    def by_url(self, url: str) -> str:
        try:
            return requests.get(url).text
        except requests.exceptions.RequestException as e:
            _logger.error(e)
            raise LoadFileError(f'Unable to load file by given url: {url}')
