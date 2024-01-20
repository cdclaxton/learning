# Counts the leaf elements in nested lists using recursion


def count_leaf_elements(x):
    assert isinstance(x, list)

    total = 0
    for xi in x:
        if isinstance(xi, list):
            total += count_leaf_elements(xi)
        else:
            total += 1

    return total


if __name__ == "__main__":
    x = [1, 2, 3]
    assert count_leaf_elements(x) == 3

    x = [1, [2, 3], 4]
    assert count_leaf_elements(x) == 4

    x = [1, [2, 3, [4, 5]], 6]
    assert count_leaf_elements(x) == 6
