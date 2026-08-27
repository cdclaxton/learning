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


def build_projection_matrix(k_x, k_y, k_z):
    return np.array([
        [k_x, 0, 0, 0],
        [0, k_y, 0, 0],
        [0, 0, k_z, 0],
        [0, 0, 0, 1],
    ])

u = np.linspace(0, 2*np.pi, 80)
v = np.linspace(0, 2*np.pi, 80)
U, V = np.meshgrid(u, v)

X = (3 + np.cos(V/2) * np.sin(U) - np.sin(V/2) * np.sin(2*U)) * np.cos(V) + 6
Y = (3 + np.cos(V/2) * np.sin(U) - np.sin(V/2) * np.sin(2*U)) * np.sin(V) + 6
Z = np.sin(V/2) * np.sin(U) + np.cos(V/2) * np.sin(2*U) + 5

m, n = np.shape(X)

S1 = array_packing(X, Y, Z)
S2 = build_projection_matrix(0, 1, 1) @ S1  # yz-axis
S3 = build_projection_matrix(1, 0, 1) @ S1  # xz-axis
S4 = build_projection_matrix(1, 1, 0) @ S1  # xy-axis

fig = go.Figure(homogeneous_coords_to_surface(S1, m, n))
fig.add_trace(homogeneous_coords_to_surface(S2, m, n, 0.2))
fig.add_trace(homogeneous_coords_to_surface(S3, m, n, 0.2))
fig.add_trace(homogeneous_coords_to_surface(S4, m, n, 0.2))
fig.show()