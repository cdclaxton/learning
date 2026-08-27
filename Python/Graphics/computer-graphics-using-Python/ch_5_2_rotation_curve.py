import numpy as np
import plotly.express as px

u = np.linspace(0, 2 * np.pi, 500)
r = np.exp(np.cos(u)) - 2 * np.cos(4 * u) + (np.sin(u / 12)) ** 5
x = r * np.sin(u) + 4
y = r * np.cos(u)

# Curve
C1 = np.array([x, y, np.ones(len(x))])

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

# Rotate curve
C2 = RM @ C1

# Plot
fig = px.line(x=C1[0, :], y=C1[1, :])
fig.add_trace(px.line(x=C2[0, :], y=C2[1, :]).data[0])
fig.update_traces(line_color="black", line_width=4)
fig.update_yaxes(scaleanchor="x")
fig.show()
