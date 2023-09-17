# Calculate posterior probabilities of the entities given the text for
# different values of p_m (the probability that a token is missing).


def posterior_probs(p_m):
    """Calculate the posterior probabilities p(E|T)."""
    assert 0.0 <= p_m <= 1.0, f"invalid probability: {p_m}"

    denominator = (
        (1 - p_m) ** 3 + ((1 - p_m) ** 3) * p_m + ((1 - p_m) ** 3) * (p_m**2)
    )

    return [
        0,
        ((1 - p_m) ** 3) / denominator,
        ((1 - p_m) ** 3 * p_m) / denominator,
        ((1 - p_m) ** 3 * p_m**2) / denominator,
    ]


def show_posterior_probs(p_m):
    print(f"p_m = {p_m}:")
    for i, p in enumerate(posterior_probs(p_m)):
        print(f"p(E_{i} | T) = {p}")
    print()


if __name__ == "__main__":
    show_posterior_probs(0)
    show_posterior_probs(0.1)
    show_posterior_probs(0.2)
    show_posterior_probs(0.5)
    show_posterior_probs(0.99)
