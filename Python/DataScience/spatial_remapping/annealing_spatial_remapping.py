# Annealing-based spatial remapping

import math
import matplotlib.pyplot as plt
import numpy as np


def generate_points(x_max, y_max, num_clusters, num_points):
    """Generate random points clustered around centres."""

    assert x_max > 0
    assert y_max > 0
    assert num_clusters > 0
    assert num_points > 0

    # Randomly generate the cluster centres
    cluster_centres = [
        (np.random.uniform(0, x_max), np.random.uniform(0, y_max)) \
        for _ in range(num_clusters)
    ]

    sigma = min(x_max, y_max) / (num_clusters * 1.8)

    # Randomly generate the points
    X = np.zeros((num_points, 2))

    for i in range(num_points):
        # Select the cluster
        cluster_idx = np.random.randint(0, num_clusters)

        # Keep generating a point until it is in the required range
        valid = False
        while not valid:
            x = np.random.normal(cluster_centres[cluster_idx][0], sigma)
            y = np.random.normal(cluster_centres[cluster_idx][1], sigma)

            valid = (0 <= x < x_max) and (0 <= y <= y_max)

        X[i,0] = x
        X[i,1] = y

    assert X.shape[0] == num_points
    assert X.shape[1] == 2

    return X


def distances(X):
    """Returns a vector of distances from each point to every other point."""

    n = len(X)
    expected_number = int(n*(n-1) / 2)
    distances = np.zeros(expected_number)

    idx = 0
    for i in range(n):
        for j in range(i+1, n):
            distances[idx] = np.sqrt(np.sum(np.power(X[i] - X[j],2)))
            idx += 1

    assert idx == expected_number

    return distances


def p(d_original, d_proposed, threshold, delta_max, sigma):
    """Probability of the proposed distance."""

    if d_original <= threshold:
        # Use a normal distribution centred on the original distance
        # if d_proposed < threshold, otherwise the probability is close to zero
        if d_proposed <= threshold:
            return gaussian(d_proposed, d_original, sigma)
        else:
            return 1e-9

    else:
        if d_proposed < threshold:
            return 1e-9
        elif d_proposed <= d_original:
            return 1.0
        else:
            d = d_proposed - d_original
            if d < delta_max:
                return 1  - (d_proposed - d_original) / delta_max
            else:
                return 1e-9
        
    
def test_p():

    threshold = 5
    delta_max = 10
    sigma = 2
    
    test_cases = [
        {
            "name": "Same distance, below threshold",
            "d_original": 0,
            "d_proposal": 0,
            "expected": 1.0
        },
        {   
            "name": "Same distance, above threshold",
            "d_original": 20,
            "d_proposal": 20,
            "expected": 1.0
        }
    ]

    for test_case in test_cases:
        actual = p(test_case["d_original"], 
                   test_case["d_proposal"], 
                   threshold, delta_max, sigma)

        assert abs(actual - test_case["expected"]) < 1e-6, \
            f"{test_case['name']}: expected = {test_case['expected']}, actual = {actual}"


def find_alpha_beta(s_delta, delta, s_delta_h, delta_h):
    """Find the parameters of the sigmoid."""
    
    f_delta_h = np.log(1/(s_delta_h) - 1)
    f_delta = np.log(1/(s_delta) - 1)

    beta = (f_delta_h*delta - f_delta*delta_h) / (f_delta_h - f_delta)
    alpha = -f_delta / (delta - beta)

    return (alpha, beta)


def gaussian(x, mu, sigma):
    """Unnormalised Gaussian distribution."""
    return np.exp(-np.power(x-mu, 2) / np.power(2 * sigma, 2))


def sigmoid(x, alpha, beta):
    """Scaled and shifted sigmoid function."""
    return 1/(1 + np.exp(-alpha*(x-beta)))


def log_probability(d1, d2, threshold, delta_max, sigma):
    """Log probability of the difference in distances."""

    assert len(d1) == len(d2)

    N = len(d1)
    probs = [np.log(p(d1[i], d2[i], threshold, delta_max, sigma)) for i in range(N)]
    return sum(probs)
    

def perform_annealing(X, threshold, delta_max, sigma):
    """Perform simulated annealing to move points."""

    # Calculate the distances between each point to every other point for the
    # original set of points
    distances_original = distances(X)

    jitter_sigma = 3
    num_points_per_temp = int(X.shape[0] * 0.90)
    k_max = 500

    N = X.shape[0]
    X_current = np.copy(X)
    num_acceptances = 0
    num_tests = 0

    for k in range(k_max):

        # Temperate
        T = 1 - k / k_max

        # Jitter standard deviation is a function of temperate
        jitter_sigma_T = jitter_sigma * T

        for point_idx in range(X.shape[0]):

            # Make a copy of the point to jitter
            original = np.copy(X_current[point_idx])

            # Apply a jitter to the selected point
            X_current[point_idx] = X_current[point_idx] + \
                np.random.normal(0, jitter_sigma_T, (1,2))

            # Calculate the new distances between points
            distances_proposed = distances(X_current)

            # Calculate the probability of the new configuration of points
            prob = log_probability(distances_original, distances_proposed,
                                   threshold, delta_max, sigma)
            
            if np.exp(prob) > np.random.rand():
                num_acceptances += 1
            else:
                # Revert the change
                X_current[point_idx] = original
            
            num_tests += 1

    print(f"Number of proposal acceptances: {num_acceptances} / {num_tests}")
    return X_current



if __name__ == '__main__':

    # Run tests
    #test_p()

    # 
    threshold = 5
    # threshold_h = 10
    # s_threshold = 1e-3
    # s_threshold_h = 1 - 1e-3
    delta_max = 10000
    sigma = 10

    plot_prob_dist = True

    if plot_prob_dist:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        dists = np.arange(0, 20, 0.01)
        d_original = threshold*2
        sub_threshold = [p(threshold/2, d_proposed, threshold, delta_max, sigma) \
                        for d_proposed in dists]
        
        above_threshold = [p(d_original, d_proposed, threshold, delta_max, sigma) \
                        for d_proposed in dists]

        ax1.plot(dists, sub_threshold)
        ax1.axvline(threshold, c='r')
        ax1.set_title('Original point below threshold')
        ax1.set_xlabel('Proposed distance')
        ax1.set_ylabel('Probability')

        ax2.plot(dists, above_threshold)
        ax2.axvline(threshold, c='r')
        ax2.axvline(d_original, c='g')
        ax2.set_title('Original point above threshold')
        ax2.set_xlabel('Proposed distance')
        ax2.set_ylabel('Probability')
        plt.show()

    # Generate the random points
    x_max = 100
    y_max = 100
    num_points = 10
    X = generate_points(x_max, y_max, 6, num_points)

    # Perform annealing
    X_prime = perform_annealing(X, threshold, delta_max, sigma)

    # Define colours for the points as a function of their original 
    # (x,y) coordinates
    colors = np.zeros((X.shape[0], 3))
    for i in range(X.shape[0]):
        red = X[i,0] / x_max
        blue = X[i,1] / y_max
        green = 0.3 * (0.5*red + 0.25*blue)
        colors[i] = [red, green, blue]

    # Plot the original and mapped points
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.scatter(X[:,0], X[:,1], c=colors)
    for i in range(num_points):
        ax1.text(X[i,0], X[i,1], str(i+1), fontsize="xx-small")
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title("Original points")

    for i in range(X.shape[0]):
        for j in range(i+1, X.shape[0]):
            d = np.sqrt(np.sum(np.power(X[i] - X[j],2)))
            if d < threshold:
                ax1.plot([X[i,0], X[j,0]], 
                         [X[i,1], X[j,1]], 'k-')

    ax2.scatter(X_prime[:,0], X_prime[:,1], c=colors)
    for i in range(num_points):
        ax2.text(X_prime[i,0], X_prime[i,1], str(i+1), fontsize="xx-small")
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')  
    ax2.set_title("Mapped points")      

    for i in range(X_prime.shape[0]):
        for j in range(i+1, X_prime.shape[0]):
            d = np.sqrt(np.sum(np.power(X_prime[i] - X_prime[j],2)))
            if d < threshold:
                ax2.plot([X_prime[i,0], X_prime[j,0]], 
                         [X_prime[i,1], X_prime[j,1]], 'k-')

    plt.show()    