from likelihood.likelihood_add_remove import (
    make_likelihood_symmetric,
    num_token_additions_removals,
)


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
        {
            "actual": ["A", "C"],
            "entity": ["A", "B"],
            "expected_added": 1,
            "expected_removed": 1,
        },
    ]

    for test_case in test_cases:
        expected_added = test_case["expected_added"]
        expected_removed = test_case["expected_removed"]
        num_token_additions_removals(
            test_case["actual"], test_case["entity"]
        ) == expected_added, expected_removed


def test_make_likelihood_symmetric():
    x0 = 0.2
    p0 = 0.9
    x1 = 0.5
    p1 = 0.1
    likelihood_fn = make_likelihood_symmetric(x0, p0, x1, p1)

    assert (
        likelihood_fn.calc(["7", "straight", "street"], ["7", "straight", "street"])
        == 1.0
    )


def test_min_count():
    likelihood = make_likelihood_symmetric(0.2, 0.9, 0.5, 0.1)

    # n = 5
    # for i in range(n):
    #     num_matching = n - i
    #     print(f"{num_matching}: {likelihood._calc_prob(n, 0, i)}")

    assert likelihood.min_count(4, 0.2) == 3
    assert likelihood.min_count(5, 0.6) == 4
