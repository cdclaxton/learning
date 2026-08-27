import numpy as np
import plotly.express as px

# Origin in the global coordinate system
pi = [6, 5, 1]

# Local coordinate system
LC = np.array([[1, 0, pi[0]], [0, 1, pi[1]], [0, 0, pi[2]]])

# Plot the local coordinate system
x = [
    LC[0, 0] + LC[0, 2],
    LC[0, 2],
    LC[0, 1] + LC[0, 2],
]

y = [LC[1, 0] + LC[1, 2], LC[1, 2], LC[1, 1] + LC[1, 2]]

fig = px.line(x=x, y=y)
fig.update_traces(line_color="red", line_width=4)
fig.show()
