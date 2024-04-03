from entity.matcher_add_remove import (
    EntityMatcherAddRemove,
    adds_removes_from_positions,
    calc_window_positions,
)
from likelihood.likelihood_add_remove import (
    LikelihoodAddRemoveFn,
    make_likelihood_add_remove_symmetric,
)
from lookup.in_memory_lookup import InMemoryLookup


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


def test_calc_window_positions():
    """Unit tests for calc_window_positions()."""

    # Boundary:  |        |
    # Indices:   0  1  2  3  4  5  6  7
    # Windows:   =======
    #               =======
    assert list(calc_window_positions(0, 3, 3, 3)) == [
        (0, 2),
        (1, 3),
    ]

    # Boundary:        |        |
    # Indices:   0  1  2  3  4  5  6  7
    # Windows:         =======
    #                     =======
    assert list(calc_window_positions(2, 5, 3, 3)) == [
        (2, 4),
        (3, 5),
    ]

    # Boundary:  |        |
    # Indices:   0  1  2  3  4  5  6  7
    # Windows:   ==========
    assert list(calc_window_positions(0, 3, 4, 4)) == [
        (0, 3),
    ]

    # Boundary:        |        |
    # Indices:   0  1  2  3  4  5  6  7
    # Windows:         ==========
    assert list(calc_window_positions(2, 5, 4, 4)) == [
        (2, 5),
    ]

    # Boundary:        |        |
    # Indices:   0  1  2  3  4  5  6  7
    assert list(calc_window_positions(2, 5, 5, 5)) == []

    # Boundary:  |        |
    # Indices:   0  1  2  3  4  5  6  7
    # Windows:   ====
    #            =======
    #            ==========
    #               ====
    #               =======
    #                  ====
    assert list(calc_window_positions(0, 3, 2, 4)) == [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    ]

    # Boundary:     |              |
    # Indices:   0  1  2  3  4  5  6  7
    # Windows:      ==========
    #               =============
    #                  ==========
    #                  =============
    #                      ==========
    assert list(calc_window_positions(1, 6, 4, 5)) == [
        (1, 4),
        (1, 5),
        (2, 5),
        (2, 6),
        (3, 6),
    ]


# def test_calc_adds_removes():

#     # Make an in-memory lookup
#     lookup = InMemoryLookup()
#     lookup.add(1, ["78", "straight", "street"])
#     lookup.add(2, ["78", "broad", "street"])
#     lookup.add(3, ["81", "straight", "street", "swindon"])

#     n_e1 = 3
#     n_e2 = 3
#     n_e3 = 4

#     # Make a matcher
#     likelihood = make_likelihood_add_remove_symmetric(2, 0.9, 5, 0.3)
#     matcher = EntityMatcherAddRemove(lookup, likelihood, 3, 4, 0.0, 5)

#     # Token index:     0       1        2           3         4
#     text_tokens = ["address", "78", "straight", "street", "swindon"]
#     for token in text_tokens:
#         matcher.next_token(token)

#     # Token index:  |    0    |  1  |     2     |    3    |    4    |
#     # Entities:     |         | e-1 | e-1       | e-1     |         |
#     #               |         | e-2 |           | e-2     |         |
#     #               |         | e-3 | e-3       | e-3     |         |
#     # Text tokens:  | address | 78  | straight  | street  | swindon |

#     assert matcher._calc_adds_removes(1, 1, 3, n_e1) == (0, 0)
#     assert matcher._calc_adds_removes(1, 1, 4, n_e1) == (1, 0)
#     assert matcher._calc_adds_removes(1, 1, 2, n_e1) == (0, 1)

#     assert matcher._calc_adds_removes(2, 1, 3, n_e2) == (1, 1)
#     assert matcher._calc_adds_removes(2, 0, 3, n_e2) == (2, 1)

#     assert matcher._calc_adds_removes(3, 1, 4, n_e3) == (1, 1)
#     assert matcher._calc_adds_removes(3, 0, 1, n_e3) == (2, 4)
#     assert matcher._calc_adds_removes(3, 0, 4, n_e3) == (2, 1)
