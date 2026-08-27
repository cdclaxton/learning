import numpy as np
import plotly.graph_objects as go

u = np.linspace(0, 2*np.pi, 80)
v = np.linspace(0, 2*np.pi, 80)
U, V = np.meshgrid(u, v)

a, b, c, p = 3, 6, 8, 1
r = c + a*np.cos(U) * np.cos(p*V) * b * np.sin(U) * np.sin(p*V)
X = r * np.cos(V) + 4
Y = r * np.sin(V) + 20
Z = a * np.cos(U) * np.sin(p*V) + b * np.sin(U) * np.cos(p*V) + 3

# Perform array packing
m, n = np.shape(X)
S1 = np.ones((4, m*n))
for row in range(m):
    S1[0:3, row*n:(row+1)*n] = [X[row,:], Y[row,:], Z[row,:]]

# Unit normal vector for the reflection
nv = np.array([[1],[2],[5],[0]])
nv = nv / np.linalg.norm(nv)
      
# Householder reflection
Hn = np.eye(4) - 2*(nv @ nv.T)
S2 = Hn @ S1

def homogeneous_coords_to_surface(S, m, n, colorscale='inferno'):

    # Perform array unpacking
    X = np.zeros((m,n))
    Y = np.zeros((m,n))
    Z = np.zeros((m,n))
    for row in range(m):
        X[row, :] = S[0, row*n:(row+1)*n]
        Y[row, :] = S[1, row*n:(row+1)*n]
        Z[row, :] = S[2, row*n:(row+1)*n]

    # Return the surface
    return go.Surface(x=X, y=Y, z=Z, opacity=1, 
                      colorscale=colorscale,
                      showscale=False)
    

# Plot
fig = go.Figure(homogeneous_coords_to_surface(S1, m, n, 'inferno'))
fig.add_trace(homogeneous_coords_to_surface(S2, m, n, 'inferno'))
fig.update_yaxes(scaleanchor="x")
fig.show()