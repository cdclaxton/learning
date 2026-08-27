import matplotlib.pyplot as plt
import numpy as np

u = np.linspace(1, 4, 4)
v = np.linspace(3, 7, 5)
U, V = np.meshgrid(u, v)

X = U**2 * V + 150
Y = U * V**3

m, n = np.shape(X)
for row in range(m - 1):
    for col in range(n - 1):
        x = [X[row, col], X[row + 1, col], X[row + 1, col + 1], X[row, col + 1]]
        y = [Y[row, col], Y[row + 1, col], Y[row + 1, col + 1], Y[row, col + 1]]
        plt.fill(x, y, color="green", alpha=0.4)

plt.show()
