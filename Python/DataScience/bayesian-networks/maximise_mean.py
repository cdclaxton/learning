#
import numpy as np
from collections import defaultdict
from itertools import combinations


def random_distribution(max_value):
    """Generate a random discrete probability distribution."""

    assert type(max_value) == int and max_value > 0

    p = np.ones(max_value)
    d = np.random.dirichlet(p)

    return {i: p for i, p in enumerate(d)}


def mean_of_distribution(d):
    """Mean of a distribution represented in a sparse form."""

    assert type(d) == dict

    total = 0.0
    for i, p in d.items():
        total += i * p

    return total


def prob_distribution_valid(dist):
    """Is the (sparse) probability distribution valid?"""

    assert type(dist) == dict
    return (sum(dist.values()) - 1.0) < 1e-5 and all(
        [type(k) == float or type(k) == int for k in dist.keys()]
    )


def dist_sum_two_rvs(x, y):
    """Distribution of the sum of two random variables."""

    assert prob_distribution_valid(x)
    assert prob_distribution_valid(y)

    result = defaultdict(int)

    for key1 in x.keys():
        for key2 in y.keys():
            total = key1 + key2
            result[total] += x[key1] * y[key2]

    result = dict(result)

    assert prob_distribution_valid(result)
    return result


def dist_sum_of_rvs(dists):
    """Distribution of the sum of random variables."""

    assert len(dists) >= 2
    assert all([prob_distribution_valid(d) for d in dists])

    # Distribution of the sum of the first two random variables
    result = dist_sum_two_rvs(dists[0], dists[1])

    for idx in range(2, len(dists)):
        result = dist_sum_two_rvs(result, dists[idx])

    assert prob_distribution_valid(result)
    return result


def highest_mean_pair(dists):
    assert type(dists) == list and len(dists) >= 2

    y = [(i, mean_of_distribution(dists[i])) for i in range(len(dists))]
    s = sorted(y, key=lambda x: x[1], reverse=True)[:2]
    idxs = [si[0] for si in s]

    return idxs[0], idxs[1]


def highest_mean_sum_pair(dists):
    pair_to_mean_of_sum = []
    idxs = list(range(len(dists)))
    for subset in combinations(idxs, 2):
        dist0 = dists[subset[0]]
        dist1 = dists[subset[1]]

        mu = mean_of_distribution(dist_sum_two_rvs(dist0, dist1))
        pair_to_mean_of_sum.append((subset, mu))

    s = sorted(pair_to_mean_of_sum, key=lambda x: x[1], reverse=True)

    return s[0]


def same_idxs(idx0, idx1):
    assert type(idx0) == list and len(idx0) == 2, f"idx0: {idx0}"
    assert type(idx1) == list and len(idx1) == 2, f"idx1: {idx1}"

    if idx0 == idx1:
        return True

    idx0[0], idx0[1] = idx0[1], idx0[0]

    return idx0 == idx1


if __name__ == "__main__":
    for _ in range(1000):
        # Generate N distributions
        N = 4
        dists = []
        for i in range(N):
            dists.append(random_distribution(4))

        # Find the pair of distributions that have the highest individual means
        idx0, idx1 = highest_mean_pair(dists)
        highest_mean_1 = mean_of_distribution(
            dist_sum_two_rvs(dists[idx0], dists[idx1])
        )

        idxs_approach_1 = [idx0, idx1]

        r = highest_mean_sum_pair(dists)
        idxs_approach_2 = list(r[0])

        if not same_idxs(idxs_approach_1, idxs_approach_2):
            print(f"Mean using 2 dists with highest means: {highest_mean_1}")
            print(r[1])
