from typing import NamedTuple


class InventoryItem(NamedTuple):
    quantity: int
    cost: float

    @property
    def value(self) -> float:
        return self.quantity * self.cost
