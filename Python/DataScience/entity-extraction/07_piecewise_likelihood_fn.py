# Displays a piecewise likelihood function
import matplotlib.pyplot as plt
import numpy as np

from likelihood.piecewise_linear import piecewise_likelihood


if __name__ == "__main__":
    x = np.arange(0, 1, 0.01)

    x0 = 0.2
    p0 = 0.9
    x1 = 0.5
    p1 = 0.1
    prob = [piecewise_likelihood(x0, p0, x1, p1, xi) for xi in x]

    plt.vlines(x0, 0, 1, color="red", linestyles="dotted")
    plt.hlines(p0, 0, 1, color="red", linestyles="dotted")
    plt.vlines(x1, 0, 1, color="green", linestyles="dotted")
    plt.hlines(p1, 0, 1, color="green", linestyles="dotted")
    plt.plot(x, prob)
    plt.xlabel("Proportion")
    plt.ylabel("Probability")
    plt.xlim(0, 1)
    plt.ylim(0, 1.01)
    plt.show()
