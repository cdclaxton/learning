# Signmoid through 2 points

import numpy as np
import matplotlib.pyplot as plt

def find_alpha_beta(s_delta, delta, s_delta_h, delta_h):
    """Find the parameters of the sigmoid."""
    
    f_delta_h = np.log(1/(s_delta_h) - 1)
    f_delta = np.log(1/(s_delta) - 1)

    beta = (f_delta_h*delta - f_delta*delta_h) / (f_delta_h - f_delta)
    alpha = -f_delta / (delta - beta)

    return (alpha, beta)


def sigmoid(x, alpha, beta):
    return 1/(1 + np.exp(-alpha*(x-beta)))

if __name__ == '__main__':

    # Lower bound
    s_delta = 1e-3
    delta = 2

    # Upper bound
    s_delta_h = 1 - 1e-3
    delta_h = 7

    # Find the parameters of the sigmoid
    alpha, beta = find_alpha_beta(s_delta, delta, s_delta_h, delta_h)

    # Plot the sigmoid
    x_min = -5
    x_max = 10

    x = np.arange(x_min, x_max, 0.01)
    s = sigmoid(x, alpha, beta)

    plt.plot(x, s)
    plt.axvline(delta, c='r')
    plt.axvline(delta_h, c='r')
    plt.xlabel('x')
    plt.ylabel('s(x)')
    plt.show()
