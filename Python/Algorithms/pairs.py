# Algorithm to generate all pairings of elements of two vectors
import itertools


def pairs(x, y):
    """Generate all pairs of elements of x and y."""
    assert len(x) == len(y)

    N = len(x)
    all_pairs = []

    for seq in itertools.permutations(y):
        all_pairs.append([(x[i], seq[i]) for i in range(N)])

    return all_pairs


if __name__ == "__main__":
    # One element
    x = [1]
    y = [5]
    assert pairs(x, y) == [[(1, 5)]]

    # Two elements
    x = [1, 2]
    y = [5, 6]
    assert pairs(x, y) == [[(1, 5), (2, 6)], [(1, 6), (2, 5)]]

    # Three elements
    x = [1, 2, 3]
    y = [5, 6, 7]
    assert pairs(x, y) == [
        [(1, 5), (2, 6), (3, 7)],
        [(1, 5), (2, 7), (3, 6)],
        [(1, 6), (2, 5), (3, 7)],
        [(1, 6), (2, 7), (3, 5)],
        [(1, 7), (2, 5), (3, 6)],
        [(1, 7), (2, 6), (3, 5)],
    ]
