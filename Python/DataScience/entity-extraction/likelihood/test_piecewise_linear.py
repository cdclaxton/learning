from likelihood.piecewise_linear import piecewise_likelihood


def test_piecewise_linear():
    assert piecewise_likelihood(0.2, 0.9, 0.5, 0.1, 0.0) == 1
    assert piecewise_likelihood(0.2, 0.9, 0.5, 0.1, 1.0) == 0.1
