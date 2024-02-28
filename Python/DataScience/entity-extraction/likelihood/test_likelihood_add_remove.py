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
    n_max = 3
    likelihood_fn = make_likelihood_symmetric(x0, p0, x1, p1, n_max)

    assert (
        likelihood_fn.calc(["7", "straight", "street"], ["7", "straight", "street"])
        == 1.0
    )


def test_min_count():
    likelihood = make_likelihood_symmetric(0.2, 0.9, 0.5, 0.1, 5)

    assert likelihood.min_count(4, 0.2) == 3
    assert likelihood.min_count(5, 0.6) == 4


def test_lookup_is_consistent():
    n_max = 5
    likelihood = make_likelihood_symmetric(0.2, 0.9, 0.5, 0.1, n_max)

    for n_tokens in range(1, n_max + 1):
        for num_adds in range(n_max + 1):
            for num_removes in range(n_max + 1):
                p_calc = likelihood._calc_prob(n_tokens, num_adds, num_removes)
                p_lookup = likelihood._calc_prob_using_lookup(
                    n_tokens, num_adds, num_removes
                )
                assert abs(p_calc - p_lookup) < 1e-7
