import matplotlib.pyplot as plt
import numpy as np

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, 1, 8)

U, V = np.meshgrid(u, v)

r = (10 * V + 3 * np.cos(np.sin(6 * U))) / 20
X = (r * (2 * np.cos(U) + np.cos(2 * U))) / 2
Y = r * (2 * np.sin(U) - np.sin(2 * U))

m, n = np.shape(X)


def x_y_to_homogeneous(X, Y):
    S = np.ones((3, m * n))
    for row in range(m):
        S[0:2, row * n : (row + 1) * n] = [X[row, :], Y[row, :]]

    return S


# Create the surface in homogenous coordinates
S1 = x_y_to_homogeneous(X, Y)


def build_translation_matrix(p):
    return np.array(
        [
            [1, 0, p[0]],
            [0, 1, p[1]],
            [0, 0, p[2]],
        ]
    )


def build_rotation_matrix(theta):
    return np.array(
        [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ]
    )


TM = build_translation_matrix([-0.5, 1.5, 1])
RM = build_rotation_matrix(-60 * np.pi / 180)

TTM = TM @ RM @ np.linalg.inv(TM)
S2 = TTM @ S1


def unpack_array(S, m, n):
    X = np.zeros((m, n))
    Y = np.zeros((m, n))
    for row in range(m):
        X[row, :] = S[0, row * n : (row + 1) * n]
        Y[row, :] = S[1, row * n : (row + 1) * n]

    return X, Y


X2, Y2 = unpack_array(S2, m, n)


def plot_surface(X, Y):
    for row in range(m - 1):
        for col in range(n - 1):
            x = [X[row, col], X[row + 1, col], X[row + 1, col + 1], X[row, col + 1]]
            y = [Y[row, col], Y[row + 1, col], Y[row + 1, col + 1], Y[row, col + 1]]
            plt.fill(x, y, color="green", alpha=0.4)


plot_surface(X, Y)
plot_surface(X2, Y2)
plt.show()
