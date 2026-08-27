import numpy as np
import plotly.graph_objects as go

u = np.linspace(0, 2*np.pi, 80)
v = np.linspace(0, np.pi, 80)
U,V = np.meshgrid(u, v)

X = (2 + np.sin(7*u)) * np.cos(U) * np.sin(V)
Y  = V
Z = (2 + np.sin(7*u)) * np.sin(U) * np.sin(V)

# Perform array packing
m,n = np.shape(X)
S1 = np.ones((4,m*n))
for row in range(m):
    S1[0:3, row*n:(row+1)*n] = [X[row,:], Y[row,:], Z[row,:]]

def build_translation_matrix(p):
    return np.array([
        [1,0,0,p[0]],
        [0,1,0,p[1]],
        [0,0,1,p[2]],
        [0,0,0,p[3]],
    ])

TM = build_translation_matrix([-4, 5, -2, 1])
S2 = TM @ S1

# Perform array unpacking
X2 = np.zeros((m,n))
Y2 = np.zeros((m,n))
Z2 = np.zeros((m,n))
for row in range(m):
    X2[row, :] = S2[0, row*n:(row+1)*n]
    Y2[row, :] = S2[1, row*n:(row+1)*n]
    Z2[row, :] = S2[2, row*n:(row+1)*n]

fig = go.Figure(go.Surface(x=X, y=Y, z=Z, opacity=1, colorscale='solar', showscale=False))
fig.add_trace(go.Surface(x=X2, y=Y2, z=Z2, opacity=1, colorscale='solar', showscale=False))
fig.update_yaxes(scaleanchor="x")
fig.show()