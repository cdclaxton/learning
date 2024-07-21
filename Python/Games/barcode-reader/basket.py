import math
from dataclasses import dataclass

from loyalty import LoyaltyMember


@dataclass
class StockItem:
    barcode: bytes
    cost_in_pence: int
    points: int


class StockControl:
    def __init__(self, default_price: int):
        self._default_price = default_price

    @staticmethod
    def _points(cost_in_pence):
        return int(math.floor(cost_in_pence / 10))

    def lookup(self, barcode: bytes):
        """Lookup an item given its barcode."""

        if len(barcode) == 0:
            cost = self._default_price
        else:
            b = str(int(barcode))
            try:
                cost = 100 * int(b[-3]) + 10 * int(b[-2]) + int(b[-1])
            except:
                cost = self._default_price

        return StockItem(
            barcode=barcode, cost_in_pence=cost, points=StockControl._points(cost)
        )


class Basket:
    """Basket of items."""

    def __init__(self):
        self._items: list[StockItem] = []
        self.loyalty_member: LoyaltyMember | None = None
        self._points_applied = False

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def add_item(self, item: StockItem):
        assert type(item) == StockItem
        self._items.append(item)
        self._update_loyalty()

    def _update_loyalty(self):
        if self.loyalty_member is None:
            return

        if not self._points_applied:
            for item in self._items:
                self.loyalty_member.add_points(item.points)
            self._points_applied = True
        else:
            self.loyalty_member.add_points(self._items[-1].points)

    def add_loyalty(self, member: LoyaltyMember) -> None:
        assert member is not None
        assert type(member) == LoyaltyMember

        if self.loyalty_member is None:
            self.loyalty_member = member
            self._update_loyalty()

    def last_item_cost(self):
        return self._items[-1].cost_in_pence

    def total_cost(self):
        return sum([item.cost_in_pence for item in self._items])
