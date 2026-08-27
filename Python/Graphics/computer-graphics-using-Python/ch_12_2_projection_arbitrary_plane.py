import numpy as np
import plotly.graph_objects as go

def array_packing(X, Y, Z):
    # Perform array packing
    m, n = np.shape(X)
    S = np.ones((4, m*n))
    for row in range(m):
        S[0:3, row*n:(row+1)*n] = [X[row,:], Y[row,:], Z[row,:]]

    return S


def homogeneous_coords_to_surface(S, m, n, opacity=1, colorscale='inferno'):

    # Perform array unpacking
    X = np.zeros((m,n))
    Y = np.zeros((m,n))
    Z = np.zeros((m,n))
    for row in range(m):
        X[row, :] = S[0, row*n:(row+1)*n]
        Y[row, :] = S[1, row*n:(row+1)*n]
        Z[row, :] = S[2, row*n:(row+1)*n]

    # Return the surface
    return go.Surface(x=X, y=Y, z=Z, 
                      opacity=opacity, 
                      colorscale=colorscale,
                      showscale=False)


u = np.linspace(0, 2*np.pi, 80)
v = np.linspace(0, 2*np.pi, 80)
U, V = np.meshgrid(u, v)

X = (3 + np.cos(V/2) * np.sin(U) - np.sin(V/2) * np.sin(2*U)) * np.cos(V) + 6
Y = (3 + np.cos(V/2) * np.sin(U) - np.sin(V/2) * np.sin(2*U)) * np.sin(V) + 6
Z = np.sin(V/2) * np.sin(U) + np.cos(V/2) * np.sin(2*U) + 5

m, n = np.shape(X)

S1 = array_packing(X, Y, Z)

# Variation of the Householder matrix
nv = np.array([[2], [4], [5], [0]])
nv = nv / np.linalg.norm(nv)
P = np.eye(4) - (nv @ nv.T)
S2 = P @ S1

fig = go.Figure(homogeneous_coords_to_surface(S1, m, n))
fig.add_trace(homogeneous_coords_to_surface(S2, m, n, 0.2))

# Plot the normal vector
x = [0, nv[0,0]]
y = [0, nv[1,0]]
z = [0, nv[2,0]]
fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines'))
fig.show()