import requests
from inventorycalculator.errors import LoadFileError


class FileLoader:

    def by_url(self, url: str) -> str:
        try:
            return requests.get(url).text
        except requests.exceptions.RequestException as e:
            raise LoadFileError(f'Unable to load file by given url: {url}')
