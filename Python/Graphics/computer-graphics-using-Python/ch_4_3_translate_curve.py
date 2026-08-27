import numpy as np
import plotly.express as px

u = np.linspace(0, 2 * np.pi, 200)
r = 1.5 * np.sin(6 * u)
x = r * np.cos(u)
y = r * np.sin(u)

C1 = np.array([x, y, np.ones(len(x))])

# Translation
Dp = [5, 3, 1]

# Translation matrix
TM = np.array(
    [
        [1, 0, Dp[0]],
        [0, 1, Dp[1]],
        [0, 0, 1],
    ]
)

# Translated curve
C2 = TM @ C1

fig = px.line(x=C1[0, :], y=C1[1, :])
fig.add_traces(px.line(x=C2[0, :], y=C2[1, :]).data[0])
fig.update_traces(line_color="black", line_width=4)
fig.update_layout(title="Flowers", autosize=False)
fig.show()
