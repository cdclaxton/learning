import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    x = np.arange(1, 10)
    y = np.power(x, 2)

    plt.plot(x, y)
    plt.xlabel("$x$")
    plt.ylabel("$x^2$")
    plt.show()
