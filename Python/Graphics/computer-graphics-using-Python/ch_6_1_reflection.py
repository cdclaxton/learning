import numpy as np
import matplotlib.pyplot as plt

u = np.linspace(0, 6*np.pi, 200)
x = 5*np.cos(u) + 3*np.cos(5*u/3) + 6
y = 5*np.sin(u) - 3*np.sin(5*u/3) + 6

S1 = np.array([x, y, np.ones(len(x))])

# x-axis reflection matrix
R = np.array([
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, 0],
])

# y-axis reflection matrix
R = np.array([
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
])

# xy-axis reflection matrix
R = np.array([
    [-1, 0, 0],
    [0, -1, 0],
    [0, 0, 0],
])

S2 = R @ S1

plt.fill(S1[0,:], S1[1,:], color='darkblue', alpha=0.8)
plt.fill(S2[0,:], S2[1,:], color='darkblue', alpha=0.8)

plt.axis("equal")
plt.show()