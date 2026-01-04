# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "matplotlib>=3.10.8",
#     "numpy>=2.4.0",
# ]
# ///

import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    x = np.arange(1, 11)
    y = np.exp(x)

    plt.xlabel("$x$")
    plt.ylabel("$e^{x}$")
    plt.plot(x, y)
    plt.show()
