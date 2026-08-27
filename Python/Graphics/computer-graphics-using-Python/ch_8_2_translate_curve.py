import numpy as np
import plotly.express as px

u = np.linspace(-np.pi, np.pi, 500)
x = 8*np.cos(u) + 5*np.cos(4*u)
y = 8*np.sin(u) - 5*np.sin(4*u)
z = (x**2 + y**2)/10

C1 = np.array([x, y, z, np.ones(len(x))])

def build_translation_matrix(p):
    return np.array([
        [1,0,0,p[0]],
        [0,1,0,p[1]],
        [0,0,1,p[2]],
        [0,0,0,p[3]],
    ])

TM = build_translation_matrix([13,34,12,1])
C2 = TM @ C1

fig = px.line_3d(x=C1[0,:], y=C1[1,:], z=C1[2,:])
fig.add_trace(px.line_3d(x=C2[0,:], y=C2[1,:], z=C2[2,:]).data[0])
fig.update_traces(line_color='red', line_width=4)
fig.update_yaxes(scaleanchor="x")
fig.show()