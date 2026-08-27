import matplotlib.pyplot as plt
import numpy as np

# Robot arm
S1 = np.array([[0, 1, 5, 6, 5, 1], [0, 1, 1, 0, -1, -1], [1, 1, 1, 1, 1, 1]])

# Forearm
S2 = np.array(
    [
        [0, 1, 6, 6, 4, 4, 6, 6, 1],
        [0, 1, 1, 0.5, 0.5, -0.5, -0.5, -1, -1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
)

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

# Rotate the upper arm
RM = build_rotation_matrix(60*np.pi/180)
S1 = RM @ S1

TM = build_translation_matrix(S1[:,3])
RM2 = build_rotation_matrix(-10*np.pi/180)
S2 = TM @ RM2 @ S2

# Plot the robot arm
plt.fill(S1[0, :], S1[1, :], color="red", alpha=0.7)
plt.scatter(S1[0, 0], S1[1, 0], marker="o", lw=10, color="green")
plt.scatter(S1[0, 3], S1[1, 3], marker="o", lw=16, color="blue")

# Plot the forearm
plt.fill(S2[0, :], S2[1, :], color="red", alpha=0.7)
plt.scatter(S2[0, 0], S2[1, 0], marker="o", lw=16, color="blue")

plt.axis("equal")
plt.show()
