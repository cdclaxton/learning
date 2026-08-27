import numpy as np
import matplotlib.pyplot as plt

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

# Define a simple surface in homogeneous coordinates
S = np.array([
    [2,6,7],
    [2,1,3],
    [1,1,1],
])

# Plot the surface
plt.fill(S[0, :], S[1, :], color="red", alpha=0.7)

# Define the reflection line
m = 2
c = 1.5
theta = np.atan(m)

x0 = 0
y0 = m*x0 + c

x1 = 5
y1 = m*x1 + c
plt.plot([x0, x1], [y0, y1])

T = build_translation_matrix([0, c, 1])
R = build_rotation_matrix(np.pi/2 - theta)
Rf = np.array([
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])

S2 = T @ np.linalg.inv(R) @ Rf @ R @ np.linalg.inv(T) @ S

# Plot the new surface
plt.fill(S2[0, :], S2[1, :], color="red", alpha=0.7)

plt.axvline(x=0, color='black', linestyle='--')
plt.axhline(y=0, color='black', linestyle='--')

plt.axis("equal")
plt.grid()
plt.show()