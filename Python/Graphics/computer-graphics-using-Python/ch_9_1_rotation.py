import numpy as np
import plotly.express as px

u = np.linspace(0, 10*np.pi, 300)
x = u**2 * np.cos(2*u) / 100
y = u**2 * np.sin(2*u) / 100
z = u

C1 = np.array([x, y, z, np.ones(len(x))])

def build_rotation_matrix_x(theta):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1],
    ])

def build_rotation_matrix_y(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1],
    ])

def build_rotation_matrix_z(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta), np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

C2 = build_rotation_matrix_x(45*np.pi/180) @ C1
C3 = build_rotation_matrix_y(45*np.pi/180) @ C1
C4 = build_rotation_matrix_z(45*np.pi/180) @ C1

fig = px.line_3d(x=C1[0,:], y=C1[1,:], z=C1[2,:], color_discrete_sequence=['black'])
fig.add_trace(px.line_3d(x=C2[0,:], y=C2[1,:], z=C2[2,:], color_discrete_sequence=['red']).data[0])
fig.add_trace(px.line_3d(x=C3[0,:], y=C3[1,:], z=C3[2,:], color_discrete_sequence=['green']).data[0])
fig.add_trace(px.line_3d(x=C4[0,:], y=C4[1,:], z=C4[2,:], color_discrete_sequence=['blue']).data[0])
fig.update_yaxes(scaleanchor="x")
fig.show()