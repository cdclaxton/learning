from entity.matcher_add_remove import (
    adds_removes_from_positions,
)


def test_adds_removes_from_positions():
    """Unit tests for adds_removes_from_positions()."""

    # No adds, no removes
    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Matching:      * * *
    assert adds_removes_from_positions([0, 1, 2], 3, 3, 3) == [(0, 2, 0, 0)]

    # No adds, no removes
    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Matching:        * * *
    assert adds_removes_from_positions([1, 2, 3], 3, 3, 3) == [(1, 3, 0, 0)]

    # One add, one remove
    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Matching:        * *   *
    assert adds_removes_from_positions([1, 2, 4], 4, 4, 4) == [(1, 4, 1, 1)]

    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Matching:        * *   * *
    # Window 0:        =======
    # Window 1:          =====
    # Window 2:          =======
    assert adds_removes_from_positions([1, 2, 4, 5], 3, 3, 4) == [
        (1, 4, 1, 0),
        (2, 4, 1, 1),
        (2, 5, 1, 0),
    ]
