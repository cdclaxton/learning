# Two-to-one mapping
import math
import numpy as np


def normalise_x_y(x, y):
    # Set a lower bound on the values of x and y
    x = [xi if xi > min_value else 0 for xi in x]
    y = [yi if yi > min_value else 0 for yi in y]

    # Determine the scaling for x and y
    max_x = max(x)
    max_y = max(y)

    if max_x > 0:
        alpha_x = 1 / max_x
    else:
        alpha_x = 1.0

    if max_y > 0:
        alpha_y = 1 / max_y
    else:
        alpha_y = 1.0

    x = [alpha_x * xi for xi in x]
    y = [alpha_y * yi for yi in y]

    return x, y


def mapping(x, y, min_value):
    """Mapping function assuming x and y are essentially opposites."""
    assert len(x) == len(y)
    assert min_value > 0

    x, y = normalise_x_y(x, y)

    d = [x[i] - y[i] for i in range(len(x))]

    beta = max([abs(di) for di in d])
    if beta > 0:
        alpha_d = 1 / beta
    else:
        alpha_d = 1.0

    return [alpha_d * di for di in d]


def mapping_with_angles(x, y, min_value):
    assert len(x) == len(y)
    assert min_value > 0

    x, y = normalise_x_y(x, y)

    result = [0 for _ in range(len(x))]
    for i in range(len(x)):
        if x[i] == 0 and y[i] == 0:
            result[i] = 0
        elif x[i] == 0 and y[i] > 0:
            result[i] = -1
        elif x[i] > 0 and y[i] == 0:
            result[i] = 1
        else:
            result[i] = 1 - (4 / math.pi) * math.atan2(y[i], x[i])

    return result


if __name__ == "__main__":
    min_value = 1e-3

    test_cases = [
        {
            "x": [0],
            "y": [0],
            "expected": [0],
            "expected_angles": [0],
        },
        {
            "x": [10],
            "y": [0],
            "expected": [1],
            "expected_angles": [1],
        },
        {
            "x": [0],
            "y": [10],
            "expected": [-1.0],
            "expected_angles": [-1.0],
        },
        {
            "x": [10, 5],
            "y": [0, 0],
            "expected": [1, 0.5],
            "expected_angles": [1, 1],
        },
        {
            "x": [0, 0],
            "y": [10, 5],
            "expected": [-1.0, -0.5],
            "expected_angles": [-1, -1],
        },
        {
            "x": [0, 5],
            "y": [10, 0],
            "expected": [-1.0, 1.0],
            "expected_angles": [-1, 1],
        },
        {
            "x": [0, 5, 2.5],
            "y": [10, 0, 0],
            "expected": [-1.0, 1.0, 0.5],
            "expected_angles": [-1, 1, 1],
        },
        {
            "x": [0, 5, 2.5, 10],
            "y": [10, 0, 0, 10],
            "expected": [-1.0, 0.5, 0.25, 0.0],
            "expected_angles": [-1, 1, 1, 0],
        },
    ]

    for test_case in test_cases:
        x = test_case["x"]
        y = test_case["y"]
        actual = mapping(x, y, min_value)
        expected = np.array(test_case["expected"])
        assert np.allclose(
            actual, expected
        ), f"mapping: x = {x}, y = {y}, expected = {expected}, actual = {actual}"

        actual_angles = mapping_with_angles(x, y, min_value)
        expected_angles = np.array(test_case["expected_angles"])
        assert np.allclose(
            actual_angles, expected_angles
        ), f"mapping_with_angles: x = {x}, y = {y}, expected = {expected_angles}, actual = {actual_angles}"
