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