import numpy as np
import plotly.graph_objects as go

u = np.linspace(np.pi/3, 11*np.pi/15, 100)
v = np.linspace(0, 2*np.pi, 60)
U,V = np.meshgrid(u,v)

X = (1-U)*(3+np.cos(V))*np.cos(4*np.pi*U)
Y = (1-U)*(3+np.cos(V))*np.sin(4*np.pi*U)
Z = 3*U + (1-U)*np.sin(V) + 4

theta = 60*np.pi/180
rotation_axis = np.array([1.5, 2, 2])

# Unit vector
e = rotation_axis / np.linalg.norm(rotation_axis)
e1 = np.sin(theta/2) * e
F = np.cos(theta/2)

m,n = np.shape(X)
X2 = np.zeros((m,n))
Y2 = np.zeros((m,n))
Z2 = np.zeros((m,n))
for row in range(m):
    for col in range(n):
        p1 = np.array([X[row,col], Y[row,col], Z[row,col]])
        p2 = p1 + (2*F)*(np.cross(e1, p1) + 2*(np.cross(e1, np.cross(e1,p1))))
        X2[row,col] = p2[0]
        Y2[row,col] = p2[1]
        Z2[row,col] = p2[2]

fig = go.Figure(go.Surface(x=X, y=Y, z=Z, opacity=1, colorscale='inferno'))
fig.add_trace(go.Scatter3d(x=[0, 5 * rotation_axis[0]], 
                           y=[0, 5 * rotation_axis[1]],
                           z=[0, 5 * rotation_axis[2]],
                           mode='lines'))
fig.add_trace(go.Surface(x=X2, y=Y2, z=Z2, opacity=1, colorscale='deep'))
fig.show()