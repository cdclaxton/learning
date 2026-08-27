import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def draw_local_coordinate_system(LC):
    x = LC[0,3] + np.array([LC[0,0], 0, LC[0,1], 0, LC[0,2]])
    y = LC[1,3] + np.array([LC[1,0], 0, LC[1,1], 0, LC[1,2]])
    z = LC[2,3] + np.array([LC[2,0], 0, LC[2,1], 0, LC[2,2]])

    return px.line_3d(x=x, y=y, z=z)


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


# Define a local coordinate system
LC1 = np.eye(4)

# Define a second local coordinate system
LC2 = np.array([
    [-0.09, 0.98, -0.15, 1],
    [-0.49, 0.17, 0.85, 3],
    [0.866, 0, 0.5, 2],
    [0, 0, 0, 1],
])

# Define a surface
u = np.linspace(0, 2*np.pi, 70)
v = np.linspace(-np.pi, np.pi, 70)
U, V = np.meshgrid(u, v)

X = 0.2 * (U - np.sin(U)) * np.cos(V)
Y = 0.6 * (1 - np.cos(U)) * np.sin(V)
Z = 0.2 * U * 2

m, n = np.shape(X)
S1 = array_packing(X, Y, Z)

# Perform a mixed transformation
S2 = LC2 @ S1

# Plot the original local coordinate system
fig = draw_local_coordinate_system(LC1)
fig.update_traces(line_color='red', line_width=4)

# Plot the 2nd local coordinate system
fig.add_trace(draw_local_coordinate_system(LC2).data[0])
fig.update_traces(line_color='red', line_width=4)

# Plot the original surface
fig.add_trace(homogeneous_coords_to_surface(S1, m, n, 0.8))

# Plot the transformed surface
fig.add_trace(homogeneous_coords_to_surface(S2, m, n, 0.8))

fig.show()