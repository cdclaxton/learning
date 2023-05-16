import pytest

from run_experiments import *

def test_perfect_stage_probability():
    """Unit tests for perfect_stage_probability()."""

    test_cases = [
        {
            "changepoints": [],
            "tau_max": 5,
            "num_stages": 3,
            "expected": np.array([[1, 1, 1, 1, 1], 
                                  [0, 0, 0, 0, 0], 
                                  [0, 0, 0, 0, 0]])
        },
        {
            "changepoints": [1],
            "tau_max": 5,
            "num_stages": 3,
            "expected": np.array([[1, 0, 0, 0, 0], 
                                  [0, 1, 1, 1, 1], 
                                  [0, 0, 0, 0, 0]])
        },
        {
            "changepoints": [1, 3],
            "tau_max": 5,
            "num_stages": 3,
            "expected": np.array([[1, 0, 0, 0, 0], 
                                  [0, 1, 1, 0, 0], 
                                  [0, 0, 0, 1, 1]])
        }
    ]

    for idx, t in enumerate(test_cases):
        actual = perfect_stage_probability(t["changepoints"], t["num_stages"], 
                                           t["tau_max"])

        diff = actual - t["expected"]
        err = np.sum(diff**2)
        assert err < 1e-6, f"test case {idx}: actual = {actual}"

def test_stages_error_using_most_likely():
    """Unit tests for stages_error_using_most_likely()."""

    test_cases = [
        {
            "gt": np.array([
                [1, 0, 0],
                [0, 1, 1]
            ]),
            "m": np.array([
                [1, 0, 0],
                [0, 1, 1]
            ]),
            "expected_error": 0.0
        },
        {
            "gt": np.array([
                [1, 1, 0],
                [0, 0, 1]
            ]),
            "m": np.array([
                [1, 0, 0],
                [0, 1, 1]
            ]),
            "expected_error": 1.0
        },
        {
            "gt": np.array([
                [1, 1, 1],
                [0, 0, 0]
            ]),
            "m": np.array([
                [1, 0, 0],
                [0, 1, 1]
            ]),
            "expected_error": 2.0
        },             
    ]

    for test_case in test_cases:
        actual = stages_error_using_most_likely(test_case["gt"],
                                                test_case["m"])
        assert actual == test_case["expected_error"]
