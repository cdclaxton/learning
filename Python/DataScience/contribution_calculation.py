# Contribution calculation
#
# Consider a shopping receipt where the cost of items isn't known, but the
# total is. Some items are subject to offers like buy-one-get-one-free. The
# task is to determine the contribution of each item to the overall shopping
# bill.
#
# For example, suppose the receipt is:
#
# Item A   2.10
# Item B   0.99
# =============
# TOTAL    3.09
#
# As a proportion, Item A is 2.10 / 3.09 (68 percent).
#
# Suppose instead the receipt is:
#
# Item A (1)  2.10
#    BOGOF      1.05
# Item A (2)  2.10
#    BOGOF      1.05
# Item B        0.99
# ==================
# TOTAL         3.09
#
# As a propotion, each Item A is 1.05 / 3.09 (34 percent).


def no_offer_price(cost):
    return lambda x: x * cost


def test_no_offer_price():
    f = no_offer_price(100)
    assert f(0) == 0
    assert f(1) == 100
    assert f(2) == 200


def bogof_price(cost):
    def calc(quantity):
        number_in_offer = quantity // 2
        number_not_in_offer = quantity % 2

        return cost * (number_in_offer + number_not_in_offer)

    return calc


def test_bogof_price():
    f = bogof_price(100)
    assert f(0) == 0
    assert f(1) == 100
    assert f(2) == 100
    assert f(3) == 200
    assert f(4) == 200
    assert f(5) == 300


def total(items, prices):
    """Calculate the total of the items."""

    assert type(items) == list
    assert type(prices) == dict

    # Get the quantity of each item
    item_to_quantity = {}
    for item_type in set(items):
        item_to_quantity[item_type] = len([item for item in items if item == item_type])
        assert item_to_quantity[item_type] > 0

    # Calculate the cost of each type of item
    subtotal = 0.0
    for item_type, quantity in item_to_quantity.items():
        assert item_type in prices, f"item type {item_type} missing from prices"
        subtotal += prices[item_type](quantity)

    return subtotal


if __name__ == "__main__":
    # Run unit tests
    test_no_offer_price()
    test_bogof_price()
