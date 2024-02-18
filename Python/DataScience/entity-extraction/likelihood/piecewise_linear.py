def piecewise_likelihood(x0: float, p0: float, x1: float, p1: float, x: float) -> float:
    """Piecewise linear likelihood function."""

    assert type(x0) == float and 0 < x0 < 1
    assert type(p0) == float and 0 <= p0 <= 1
    assert type(x1) == float and x0 < x1 < 1
    assert type(p1) == float and 0 <= p1 <= 1
    assert isinstance(x, float) and 0.0 <= x, f"Got type={type(x)}, x={x}"

    if x < x0:
        return ((p0 - 1) / x0) * x + 1
    elif x < x1:
        return (p1 - p0) / (x1 - x0) * (x - x0) + p0

    return p1
