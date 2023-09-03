# Spatial remapping

import math
import matplotlib.pyplot as plt
import numpy as np

from scipy import optimize


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


def distance_error(d_prime, d, rate=3):
    """Distance error of d' from d."""

    return np.power(0.5*(d_prime - d), 2)


def all_squared_distances(x):
    """Returns a vector of distances to every other point."""

    n = len(x)
    expected_number = int(n*(n-1) / 2)
    distances = np.zeros(expected_number)
    
    idx = 0
    for i in range(0, n):
        for j in range(i+1, n):
            distances[idx] = np.power(x[i] - x[j],2)
            idx += 1

    assert idx == expected_number

    return distances


def local_distance_error(X, X_prime, error_fn):
    """Local distance error."""

    assert X.shape[0] == X_prime.shape[0]
    assert X.shape[1] == 2
    assert X_prime.shape[1] == 2

    d_x = all_squared_distances(X[:,0])
    d_y = all_squared_distances(X[:,1])
    d = d_x + d_y

    d_prime_x = all_squared_distances(X_prime[:,0])
    d_prime_y = all_squared_distances(X_prime[:,1])
    d_prime = d_prime_x + d_prime_y

    total_error = [error_fn(d_prime[i], d[i]) for i in range(len(d_prime_x))]

    return sum(total_error)


def centre_rotate_scale(X):
    
    # Make a copy of the matrix
    X2 = np.copy(X)

    # Centre the points
    X2[:,0] = X2[:,0] - np.mean(X[:,0])
    X2[:,1] = X2[:,1] - np.mean(X[:,1])

    # Rotate the points
    total_direction = np.sum(X2, 0)
    theta = np.arctan2(total_direction[1], total_direction[0])

    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))

    X2 = X2 @ R

    # Scale the points
    x_variance = np.var(X2[:,0])
    y_variance = np.var(X2[:,1])

    X2[:,0] = X2[:,0] / (np.sqrt(x_variance) + 1e-6)
    X2[:,1] = X2[:,1] / (np.sqrt(y_variance) + 1e-6)

    return X2


def mean_distance(X1, X2):
    diff_sq = np.power(X1 - X2, 2)
    return np.mean(np.power(np.sum(diff_sq, 1), 0.5))


def global_mean_distance(X1, X2):
    """Mean difference between centred, rotated and scaled matrices."""

    X1_prime = centre_rotate_scale(X1)
    X2_prime = centre_rotate_scale(X2)

    return mean_distance(X1_prime, X2_prime)


def jitter_matrix(seed, N, std_dev):

    # Set the seed in the random number generator
    np.random.seed(seed)

    # Generate random points
    return np.random.normal(0, std_dev, (N, 2))


def solve(X, alpha):

    assert alpha > 0

    seed = np.random.randint(0, 1e6)
    N = X.shape[0]

    # Maximum extent
    m = np.max([np.abs(np.min(X)), np.abs(np.max(X))])

    # Make the vector of bounds
    bounds = [(-1, 1) for _ in range(4)]  # Matrix bounds
    bounds.extend([(-m, m), (-m, m)])     # Translation vector bounds
    bounds.append((1e-6, 5))              # Jitter standard deviation

    # Make the function to minimise
    def f(e):
        M = np.array([
            [e[0], e[1]],
            [e[2], e[3]],
        ])

        translation = np.array([e[4], e[5]])
        X_prime = ((X + translation) @ M) + jitter_matrix(seed, N, e[6])

        return alpha * local_distance_error(X, X_prime, distance_error) + \
            (1/(global_mean_distance(X, X_prime)+1e-6))

    # Perform numerical optimisation
    x0 = 0.5 * np.ones(7)
    results = optimize.minimize(f, x0=x0, method='Nelder-Mead', bounds=bounds)

    # Best results from the optimisation
    e = results["x"]

    # Calculate the projected data points
    M = np.array([
        [e[0], e[1]],
        [e[2], e[3]],
    ])

    # Transform the original points using the best result from the optimisation
    # step
    translation = np.array([e[4], e[5]])
    X_prime = ((X + translation) @ M) + jitter_matrix(seed, N, e[6])

    print(f"Translation vector: {translation}")
    print(f"Transformation matrix: {M}")
    print(f"Jitter standard deviation: {e[6]}")

    print(f"Unscaled local distance error: {local_distance_error(X, X_prime, distance_error)}")
    print(f"Scaled local distance error: {alpha * local_distance_error(X, X_prime, distance_error)}")
    print(f"Global distance error: {1/(global_mean_distance(X, X_prime)+1e-6)}")
    
    return X_prime


if __name__ == '__main__':

    plot_original_points = False
    plot_rotated = False
    plot_distance_error_fn = False

    # Generate the random points
    x_max = 100
    y_max = 100
    num_points = 150
    X = generate_points(x_max, y_max, 6, num_points)
    
    # Show the locations of the points
    if plot_original_points:
        plt.plot(X[:,0], X[:,1], '.')
        for i in range(num_points):
            plt.text(X[i,0], X[i,1], str(i+1), fontsize="xx-small")

        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    if plot_rotated:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.scatter(X[:,0], X[:,1])
        ax1.set_title("Original")

        X2 = centre_rotate_scale(X)
        ax2.scatter(X2[:,0], X2[:,1])
        ax2.set_title("Centred, rotated and scaled")
        plt.show()

    # Plot the distance error function
    if plot_distance_error_fn:
        d_prime = np.arange(0, 10, 0.1)
        d = 5
        e = distance_error(d_prime, d, 2)
        plt.plot(d_prime, e)
        plt.axvline(x = d, color = 'r')
        plt.xlabel('d_prime')
        plt.ylabel('error')
        plt.show()
    
    # Find the mapping using an optimisation approach
    X_prime = solve(X, 0.01)

    # Define colours for the points as a function of their original 
    # (x,y) coordinates
    colors = np.zeros((X.shape[0], 3))
    for i in range(X.shape[0]):
        red = X[i,0] / x_max
        blue = X[i,1] / y_max
        green = 0.5 * (red + blue)
        colors[i] = [red, green, blue]

    # Plot the original and mapped points
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.scatter(X[:,0], X[:,1], c=colors)
    for i in range(num_points):
        ax1.text(X[i,0], X[i,1], str(i+1), fontsize="xx-small")
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title("Original points")

    ax2.scatter(X_prime[:,0], X_prime[:,1], c=colors)
    for i in range(num_points):
        ax2.text(X_prime[i,0], X_prime[i,1], str(i+1), fontsize="xx-small")
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')  
    ax2.set_title("Mapped points")      

    plt.show()
