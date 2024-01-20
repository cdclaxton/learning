import matplotlib.pyplot as plt
import numpy as np


def sample_from_distribution(d):
    """Draw a sample from a discrete distribution d."""

    return np.argmax(np.random.multinomial(1, d))


def noisy_max(d1, d2, num_samples):
    """Noisy Max of two distributions calculated numerically."""

    assert len(d1) == len(d2)
    assert num_samples > 0

    result = np.zeros(len(d1))
    for _ in range(num_samples):
        # Draw a sample from d1 and d2
        d1_sample = sample_from_distribution(d1)
        d2_sample = sample_from_distribution(d2)

        result[max(d1_sample, d2_sample)] += 1

    return result / num_samples


def mixture_model(p1, d1, p2, d2):
    """Mixture model of two distributions."""

    assert 0.0 <= p1 <= 1.0
    assert 0.0 <= p2 <= 1.0
    assert p1 + p2 - 1.0 < 1e-6
    assert len(d1) == len(d2)

    return p1 * d1 + p2 * d2


def bernoulli(probability):
    """Returns a 0 or 1 from a Bernoulli distribution."""

    return np.random.binomial(1, probability)


def weighted_noisy_max(p1, d1, p2, d2, num_samples):
    """Weighted noisy max distribution."""

    assert 0.0 <= p1 <= 1.0
    assert 0.0 <= p2 <= 1.0
    assert p1 + p2 - 1.0 < 1e-6
    assert len(d1) == len(d2)

    result = np.zeros(len(d1))
    for _ in range(num_samples):
        risks = []
        if bernoulli(p1) == 1:
            risks.append(sample_from_distribution(d1))

        if bernoulli(p2) == 1:
            risks.append(sample_from_distribution(d2))

        if len(risks) == 0:
            result[0] += 1.0
        else:
            result[max(risks)] += 1.0

    return result / np.sum(result)


def scale_dist(prob, dist):
    zero_dist = np.zeros(len(dist))
    zero_dist[0] = 1.0

    return mixture_model(prob, dist, 1 - prob, zero_dist)


def scale_and_noisy_max_dists(p1, d1, p2, d2, n_samples):
    scaled_1 = scale_dist(p1, d1)
    scaled_2 = scale_dist(p2, d2)

    return noisy_max(scaled_1, scaled_2, n_samples)


if __name__ == "__main__":
    # Define two distributions
    p1 = 0.2
    d1 = np.array([0.0, 0.2, 0.2, 0.6])

    p2 = 0.8
    d2 = np.array([0.1, 0.2, 0.5, 0.0])

    n_samples = 100000

    scale_noisy_max_result = scale_and_noisy_max_dists(p1, d1, p2, d2, n_samples)
    print(f"Scale and noisy max: {scale_noisy_max_result}")

    noisy_max_result = noisy_max(d1, d2, n_samples)
    print(f"Noisy max: {noisy_max_result}")

    mixture_model_result = mixture_model(0.2, d1, 0.8, d2)
    print(f"Mixture model: {mixture_model_result}")

    weighted_noisy_max_result = weighted_noisy_max(p1, d1, p2, d2, n_samples)
    print(f"Weighted noisy max: {weighted_noisy_max_result}")

    fig, axs = plt.subplots(2, 4)
    x = np.arange(len(d1))
    max_y = (
        np.max(
            [
                d1,
                d2,
                noisy_max_result,
                mixture_model_result,
                weighted_noisy_max_result,
            ]
        )
        + 0.01
    )

    axs[0][0].bar(x, d1)
    axs[0][0].set_title("Distribution d1")
    axs[0][0].set_xticks(x)
    axs[0][0].set_ylabel("Probability")
    axs[0][0].set_ylim(0, max_y)

    axs[0][1].bar(x, d2)
    axs[0][1].set_xticks(x)
    axs[0][1].set_title("Distribution d2")
    axs[0][1].set_ylim(0, max_y)

    fig.delaxes(axs[0][2])
    fig.delaxes(axs[0][3])

    axs[1][0].bar(x, noisy_max_result)
    axs[1][0].set_xticks(x)
    axs[1][0].set_ylabel("Probability")
    axs[1][0].set_title("Noisy max")
    axs[1][0].set_ylim(0, max_y)

    axs[1][1].bar(x, mixture_model_result)
    axs[1][1].set_xticks(x)
    axs[1][1].set_ylabel("Probability")
    axs[1][1].set_title("Mixture model")
    axs[1][1].set_ylim(0, max_y)

    axs[1][2].bar(x, weighted_noisy_max_result)
    axs[1][2].set_xticks(x)
    axs[1][2].set_ylabel("Probability")
    axs[1][2].set_title("Weighted noisy max model")
    axs[1][2].set_ylim(0, max_y)

    axs[1][3].bar(x, scale_noisy_max_result)
    axs[1][3].set_xticks(x)
    axs[1][3].set_ylabel("Probability")
    axs[1][3].set_title("Scale and noisy max model")
    axs[1][3].set_ylim(0, max_y)

    plt.show()
