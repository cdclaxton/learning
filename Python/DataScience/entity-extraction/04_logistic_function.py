# Logistic function
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    k = 10
    x0 = 0.5
    x = np.arange(0, 1.01, 0.01)
    y = 1 / (1 + np.exp(-k * (x - x0)))

    print(f"Minimum probability: {y[0]}")
    print(f"Maximum probability: {y[-1]}")

    plt.plot(x, y)
    plt.xlabel("Proportion of tokens present")
    plt.ylabel("Likelihood")
    plt.title(f"Logistic function ($k$ = {k}, $x_0$ = {x0})")
    plt.savefig("./images/logistic_function.png")
