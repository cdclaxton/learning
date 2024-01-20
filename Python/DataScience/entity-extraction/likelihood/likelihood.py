import math


def likelihood(entity_tokens, text_tokens, p_m):
    """Calculate the likelihood p(T|E)."""

    assert type(entity_tokens) == list
    assert len(entity_tokens) > 0
    assert type(text_tokens) == list
    assert len(text_tokens) > 0
    assert 0.0 <= p_m <= 1.0

    # Number of tokens present
    n_p = len(set(entity_tokens).intersection(set(text_tokens)))

    # Number of tokens missing
    n_m = len(set(entity_tokens).difference(set(text_tokens)))

    assert n_p + n_m == len(entity_tokens)

    p = ((1 - p_m) ** n_p) * (p_m**n_m)
    assert 0.0 <= p <= 1.0

    return p


def likelihood_logistic(entity_tokens, text_tokens, k, x0):
    """Calculate the likelihood p(T|E) using a logistic function."""

    assert type(entity_tokens) == list
    assert len(entity_tokens) > 0
    assert type(text_tokens) == list
    assert len(text_tokens) > 0
    assert type(k) == float
    assert type(x0) == float

    # Number of tokens present
    n_p = len(set(entity_tokens).intersection(set(text_tokens)))

    # Proportion of tokens present
    prop = n_p / len(entity_tokens)

    # Probability
    y = 1 / (1 + math.exp(-k * (prop - x0)))
    assert 0 <= y <= 1

    return y
