import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import stats


def normalise(x):
    """Normalise to the range [0,1]."""
    x = x - min(x)
    return x / max(x)


def exponential(lam, N):
    """Generate N samples from an exponential distribution in the range [0,1]."""
    return normalise(stats.expon.rvs(loc=0, scale=1 / lam, size=N))


def generate_true_leaderboard(lam, N):
    """Generate the scores of the true leaderboard with N leads."""
    return sorted(exponential(lam, N))


def generate_actual_leaderboard(scores, sigma):
    """Generate the scores of the actual leaderboard."""
    return normalise(scores + stats.norm.rvs(loc=0, scale=sigma, size=len(scores)))


def correct_order(actual_leaderboard, idx1, idx2):
    # The true leaderboard is assumed to be sorted in ascending order of score
    if idx1 >= idx2:
        return actual_leaderboard[idx1] >= actual_leaderboard[idx2]
    else:
        return actual_leaderboard[idx1] < actual_leaderboard[idx2]


def proportion_in_correct_order(leaderboard):
    """Proportion of the leads that appear in the correct order."""
    total = 0
    total_pairs = 0
    for i in range(0, len(leaderboard) - 1):
        for j in range(i + 1, len(leaderboard)):
            total_pairs += 1
            if correct_order(leaderboard, i, j):
                total += 1
    return total / total_pairs


def select_pairs_of_leads(num_leads, num_to_select):
    """Randomly select pairs of leads."""

    pairs = []
    indices_used = set()

    while len(pairs) < num_to_select:
        idx1 = random.randint(0, num_leads - 1)
        idx2 = random.randint(0, num_leads - 1)

        if idx1 == idx2 or idx1 in indices_used or idx2 in indices_used:
            continue

        pairs.append((idx1, idx2))
        indices_used.add(idx1)
        indices_used.add(idx2)

    return pairs


def proportion_pairs_in_correct_order(leaderboard, pairs):
    """Proportion of the pairs of indices that are in the correct order."""

    total_correct = 0
    for idx1, idx2 in pairs:
        if correct_order(leaderboard, idx1, idx2):
            total_correct += 1

    return total_correct / len(pairs)


def hist(samples, n_bins):
    h, bin_edges = np.histogram(samples, bins=n_bins, range=(0, 1))
    bin_width = bin_edges[1] - bin_edges[0]
    bin_centres = bin_edges[0:-1] + bin_width / 2
    return h / len(samples), bin_centres


def plot_exponential_distributions(lambda_min, lambda_max):

    n_samples = 10000
    n_bins = 20

    samples_min = exponential(lambda_min, n_samples)
    h_min, bin_centres_min = hist(samples_min, n_bins)

    samples_max = exponential(lambda_max, n_samples)
    h_max, bin_centres_max = hist(samples_max, n_bins)

    plt.plot(bin_centres_min, h_min, label="min lambda")
    plt.plot(bin_centres_max, h_max, label="max lambda")
    plt.legend()
    plt.show()


if __name__ == "__main__":

    num_leads = 100
    num_pairs_to_check = [1, 2, 3, 5, 10]
    num_samples_per_num_pairs = 50

    # lambda_min = 1e-4
    # lambda_max = 100
    # plot_exponential_distributions(lambda_min, lambda_max)

    sigma_min = 1e-5
    sigma_max = 0.5

    results = []
    experiment_idx = 0
    total_experiments = len(num_pairs_to_check) * num_samples_per_num_pairs

    for num_pairs in num_pairs_to_check:
        for _ in range(num_samples_per_num_pairs):

            print(f"Running experiment {experiment_idx}/{total_experiments}")

            # Generate a true leaderboard
            true_leaderboard = generate_true_leaderboard(1.0, num_leads)

            # Generate the actual leaderboard by perturbing the true leaderboard
            sigma = stats.uniform.rvs(loc=sigma_min, scale=sigma_max-sigma_min)
            actual_leaderboard = generate_actual_leaderboard(true_leaderboard, sigma)

            # Randomly select the pairs the user would review
            pairs = select_pairs_of_leads(num_leads, num_pairs)

            actual_correct = proportion_in_correct_order(actual_leaderboard)
            estimated_correct = proportion_pairs_in_correct_order(
                actual_leaderboard, pairs
            )

            results.append((num_pairs, actual_correct, estimated_correct))
            experiment_idx += 1

    x = np.array([r[0] for r in results]) + stats.norm.rvs(0, 0.1, size=len(results))
    y = [r[1] - r[2] for r in results]
    plt.plot(x, y, ".", alpha=0.1)
    plt.xlabel("Number of pairs")
    plt.ylabel("Error")
    plt.show()
