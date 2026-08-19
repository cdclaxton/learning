from itertools import product


def calc_joint(p_a: list[float], b_cpts, a: int, b: list[int]):
    """Calculate p(a,b) where b is a vector."""

    assert a == 0 or a == 1
    assert len(b) == len(b_cpts)

    N = len(b_cpts)

    product_term = 1

    for i in range(N):
        product_term *= b_cpts[i][a][b[i]]

    return p_a[a] * product_term


def calc_marginal(p_a: list[float], b_cpts, a: int, b: list[int]):
    p0 = calc_joint(p_a, b_cpts, a, b)
    p1 = calc_joint(p_a, b_cpts, 1 - a, b)

    return p0 / (p0 + p1)


def calc_weight(p_b, b):
    assert len(p_b) == len(b)
    product_term = 1

    for i in range(len(b)):
        if b[i] == 0:
            product_term *= 1 - p_b[i]
        else:
            product_term *= p_b[i]

    return product_term


def generate_binary(n: int) -> list[list[bool]]:
    return [list(p) for p in product([0, 1], repeat=n)]


def calc_posterior_conditional(p_a, b_cpts, p_b):
    N = len(b_cpts)

    total = 0
    for b in generate_binary(N):
        total += calc_weight(p_b, b) * calc_marginal(p_a, b_cpts, 1, b)

    return total


if __name__ == "__main__":
    # Prior probability [p(a = 0), p(a = 1)]
    p_a = [0.4, 0.6]

    # Define the CPTs p(b_i|a) for each b_i
    b_cpts = [
        [
            [0.6, 0.4],
            [0.3, 0.7],
        ],
        [
            [0.9, 0.1],
            [0.2, 0.8],
        ],
    ]

    # Soft evidence for each b_i
    p_b = [0.9, 0.7]

    # Calculate p(a|b) using Jeffrey's approach
    posterior_conditional = calc_posterior_conditional(p_a, b_cpts, p_b)
    print(f"Posterior conditional p(a|b) = {posterior_conditional}")
