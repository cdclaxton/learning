import numpy as np
import plotly.express as px

u = np.linspace(0, 6*np.pi, 400)
x = 11 * np.cos(u) - 3 * np.cos(11*u/3)
y = 11 * np.sin(u) - 3 * np.sin(11*u/3)

C1 = np.array([x, y, np.ones(len(x))])

def build_scaling_matrix(k_x, k_y):
    return np.array([
        [k_x, 0, 0],
        [0, k_y, 0],
        [0, 0, 1],
    ])

S = build_scaling_matrix(3,3)
C2 = S @ C1

fig = px.line(x=C1[0,:], y=C1[1,:])
fig.add_trace(px.line(x=C2[0,:], y=C2[1,:]).data[0])
fig.update_yaxes(scaleanchor="x")
fig.show()
