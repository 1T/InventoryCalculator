from typing import Dict


class DynamoDBTable:
    def __init__(self, table_name: str):
        self._table_name = table_name

    def put(self, item: Dict):
        pass
