from basket import Basket, StockControl, StockItem
from loyalty import LoyaltyMember


def test_stock_control():
    s = StockControl(199)
    assert s.lookup(b"") == StockItem(b"", 199, 19)
    assert s.lookup(b"54321") == StockItem(b"54321", 321, 32)


def test_basket():
    item1 = StockItem(b"123", 10, 1)
    item2 = StockItem(b"456", 20, 2)
    item3 = StockItem(b"789", 30, 5)

    # Add items -> then add loyalty member -> add another item
    member1 = LoyaltyMember("Bob", b"Bob", 50)
    b = Basket()
    assert b.is_empty()

    b.add_item(item1)
    assert len(b._items) == 1
    assert not b.is_empty()
    assert b.last_item_cost() == 10
    assert b.total_cost() == 10

    b.add_item(item2)
    assert len(b._items) == 2
    assert b.last_item_cost() == 20
    assert b.total_cost() == 30

    b.add_loyalty(member1)
    assert b.loyalty_member == member1
    assert b._points_applied
    assert member1.points == 53

    b.add_item(item3)
    assert len(b._items) == 3
    assert member1.points == 58
    assert b.last_item_cost() == 30
    assert b.total_cost() == 60

    # Try to add a different loyalty member to the basket
    member2 = LoyaltyMember("Sarah", b"Sarah", 50)
    b.add_loyalty(member2)
    assert b.loyalty_member == member1

    # Add loyalty member -> add items
    member1 = LoyaltyMember("Bob", b"Bob", 50)
    b = Basket()
    b.add_loyalty(member1)
    assert b.loyalty_member == member1

    b.add_item(item1)
    assert len(b._items) == 1
    assert member1.points == 51

    b.add_item(item2)
    assert len(b._items) == 2
    assert member1.points == 53
