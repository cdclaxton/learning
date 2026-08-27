import matplotlib.pyplot as plt
import numpy as np

# Define the surface using two matrices, X and Y
u = np.linspace(0, 2 * np.pi, 150)
v = np.linspace(1.5, 6, 10)
U, V = np.meshgrid(u, v)

r = V + np.cos(3 * np.sin(1.5 * U))
X = r * np.sin(U) ** 3 + 6
Y = r * np.cos(U) ** 3

# Perform array packing
m, n = np.shape(X)
S1 = np.ones((3, m * n))
for row in range(m):
    S1[0:2, row * n : (row + 1) * n] = [X[row, :], Y[row, :]]

# Rotation angle
theta = 120 * np.pi / 180

# Rotation matrix
RM = np.array(
    [
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1],
    ]
)

# Perform translation
S2 = RM @ S1

# Perform array unpacking
X2 = np.zeros((m, n))
Y2 = np.zeros((m, n))
for row in range(m):
    X2[row, :] = S2[0, row * n : (row + 1) * n]
    Y2[row, :] = S2[1, row * n : (row + 1) * n]


def plot_surface(X, Y):
    for row in range(m - 1):
        for col in range(n - 1):
            x = [X[row, col], X[row + 1, col], X[row + 1, col + 1], X[row, col + 1]]
            y = [Y[row, col], Y[row + 1, col], Y[row + 1, col + 1], Y[row, col + 1]]
            plt.fill(x, y, color="green", alpha=0.4)


plot_surface(X, Y)
plot_surface(X2, Y2)

ax = plt.gca()
ax.set_aspect("equal")
plt.show()
