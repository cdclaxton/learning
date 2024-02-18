from .likelihood import LikelihoodFunctionProbMissing, num_token_additions_removals


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


def test_num_token_additions_removals():
    """Unit tests for num_token_additions_removals()."""

    test_cases = [
        {
            "actual": ["A"],
            "entity": ["A"],
            "expected_added": 0,
            "expected_removed": 0,
        },
        {
            "actual": ["A", "B"],
            "entity": ["A"],
            "expected_added": 1,
            "expected_removed": 0,
        },
        {
            "actual": ["A"],
            "entity": ["A", "B"],
            "expected_added": 0,
            "expected_removed": 1,
        },
        {
            "actual": ["C", "D"],
            "entity": ["A", "B"],
            "expected_added": 0,
            "expected_removed": 2,
        },
    ]

    for test_case in test_cases:
        expected_added = test_case["expected_added"]
        expected_removed = test_case["expected_removed"]
        num_token_additions_removals(
            test_case["actual"], test_case["entity"]
        ) == expected_added, expected_removed
