import pytest
from inventorycalculator.core.parsers.inventory_parser import InventoryParser
from inventorycalculator.errors import InvalidInventoryDataFormat
from inventorycalculator.models.inventory_item import InventoryItem


def test_parse_inventory_tsv_data():
    with open('tests/data/input.txt') as f:
        items = InventoryParser().from_tsv(f.read())
    assert 36 == len(items)
    assert any(isinstance(item, InventoryItem) for item in items)


@pytest.mark.xfail(raises=InvalidInventoryDataFormat)
def test_parse_inventory_blank_data():
    InventoryParser().from_tsv('')


@pytest.mark.xfail(raises=InvalidInventoryDataFormat)
def test_parse_inventory_invalid_data():
    InventoryParser().from_tsv('fake data\nrow2')
