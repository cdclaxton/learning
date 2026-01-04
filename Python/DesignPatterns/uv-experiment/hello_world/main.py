import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    x = np.arange(0, 2 * np.pi, 0.01)
    y = np.sin(x)

    plt.plot(x, y)
    plt.xlabel("$x$")
    plt.ylabel("$\\sin(x)$")
    plt.show()
