from entity.matcher_generic import calc_windows


def test_calc_windows():
    """Unit tests for calc_windows()."""

    # Insufficient tokens
    assert list(calc_windows(num_tokens=2, min_window=3, max_window=3)) == []
    assert list(calc_windows(num_tokens=3, min_window=4, max_window=4)) == []

    # One token
    assert list(calc_windows(num_tokens=1, min_window=1, max_window=3)) == [(0, 0)]

    # Two tokens
    assert list(calc_windows(num_tokens=2, min_window=1, max_window=3)) == [
        (0, 0),
        (0, 1),
        (1, 1),
    ]
    assert list(calc_windows(num_tokens=2, min_window=2, max_window=3)) == [(0, 1)]

    # Three tokens
    assert list(calc_windows(num_tokens=3, min_window=1, max_window=3)) == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        (2, 2),
    ]

    assert list(calc_windows(num_tokens=3, min_window=1, max_window=2)) == [
        (0, 0),
        (0, 1),
        (1, 1),
        (1, 2),
        (2, 2),
    ]

    assert list(calc_windows(num_tokens=3, min_window=2, max_window=3)) == [
        (0, 1),
        (0, 2),
        (1, 2),
    ]

    assert list(calc_windows(num_tokens=3, min_window=3, max_window=3)) == [(0, 2)]

    # Four tokens
    assert list(calc_windows(num_tokens=4, min_window=2, max_window=3)) == [
        (0, 1),  # 2
        (0, 2),  # 3
        (1, 2),  # 2
        (1, 3),  # 3
        (2, 3),  # 2
    ]
