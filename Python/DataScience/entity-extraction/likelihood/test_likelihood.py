from .likelihood import likelihood


def test_likelihood():
    """Unit tests for likelihood()."""

    def is_close(x, y):
        return abs(x - y) < 1e-6

    p_m = 0.2

    # None missing
    assert is_close(likelihood(["A"], ["A"], p_m), (1 - p_m))
    assert is_close(likelihood(["A", "B"], ["A", "B"], p_m), (1 - p_m) ** 2)

    # One missing
    assert is_close(likelihood(["A", "B"], ["A"], p_m), (1 - p_m) * p_m)
    assert is_close(likelihood(["A", "B", "C"], ["A", "C"], p_m), (1 - p_m) ** 2 * p_m)

    # Two missing
    assert is_close(likelihood(["A", "B", "C"], ["A"], p_m), (1 - p_m) * p_m**2)
