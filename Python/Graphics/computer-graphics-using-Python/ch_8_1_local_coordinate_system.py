import numpy as np
import plotly.express as px

# Origin
pi = [6,5,3,1]

# Local coordinate system
LC = np.array([
    [1, 0, 0, pi[0]],
    [0, 1, 0, pi[1]],
    [0, 0, 1, pi[2]],
    [0, 0, 0, 1]
])

x = LC[0,3] + np.array([LC[0,0], 0, LC[0,1], 0, LC[0,2]])
y = LC[1,3] + np.array([LC[1,0], 0, LC[1,1], 0, LC[1,2]])
z = LC[2,3] + np.array([LC[2,0], 0, LC[2,1], 0, LC[2,2]])

fig = px.line_3d(x=x, y=y, z=z)
fig.update_traces(line_color='red', line_width=4)
fig.update_yaxes(scaleanchor="x")
fig.show()

