import csv
from io import StringIO
from inventorycalculator.errors import InvalidInventoryDataFormatError
from inventorycalculator.models.inventory_item import InventoryItem
from typing import List


class InventoryParser:

    def from_tsv(self, data: str) -> List[InventoryItem]:
        result_items = []
        try:
            header, *items = csv.reader(StringIO(data), delimiter='\t')
            quanitity_index, cost_index = header.index('Quantity'), header.index('Cost')
            for item in items:
                result_items.append(
                    InventoryItem(
                        int(item[quanitity_index]),
                        float(item[cost_index])
                    )
                )
        except ValueError:
            raise InvalidInventoryDataFormatError('Unable to parse the given data')
        return result_items
