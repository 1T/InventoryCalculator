from typing import NamedTuple
from unittest.mock import MagicMock


class MockResponse(NamedTuple):
    text: str


class MockS3Body(NamedTuple):
    read: MagicMock
