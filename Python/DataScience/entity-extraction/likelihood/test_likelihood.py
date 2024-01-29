from .likelihood import LikelihoodFunctionProbMissing


def test_likelihood_missing_prob():
    """Unit tests for LikelihoodFunctionProbMissing class."""

    def is_close(x, y):
        return abs(x - y) < 1e-6

    p_m = 0.2

    likelihood = LikelihoodFunctionProbMissing(p_m)

    # None missing
    assert is_close(likelihood.calc(["A"], ["A"]), (1 - p_m))
    assert is_close(likelihood.calc(["A", "B"], ["A", "B"]), (1 - p_m) ** 2)

    # One missing
    assert is_close(likelihood.calc(["A"], ["A", "B"]), (1 - p_m) * p_m)
    assert is_close(likelihood.calc(["A", "C"], ["A", "B", "C"]), (1 - p_m) ** 2 * p_m)

    # Two missing
    assert is_close(likelihood.calc(["A"], ["A", "B", "C"]), (1 - p_m) * p_m**2)
