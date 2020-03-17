import pytest
from unittest.mock import patch
from inventorycalculator.core.loaders.file_loader import FileLoader
from inventorycalculator.errors import LoadFileError
from tests.mocks import MockResponse


@patch('requests.get')
def test_load_file(mock_get):
    mock_get.return_value = MockResponse(text='fake response')
    url = 'https://etix-pdf-dev.s3.amazonaws.com/9147_10832__0-10-5_7-5-2019.txt'

    assert 'fake response' == FileLoader().by_url(url)


@pytest.mark.xfail(raises=LoadFileError)
def test_load_file_fake_url():
    FileLoader().by_url('https://fake_url')
