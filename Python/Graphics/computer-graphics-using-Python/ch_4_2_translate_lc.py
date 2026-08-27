import numpy as np
import plotly.express as px


def calc_x_y_for_lc(LC):
    """Calculate x and y for plotting the local coordinate system."""
    x = [
        LC[0, 0] + LC[0, 2],
        LC[0, 2],
        LC[0, 1] + LC[0, 2],
    ]

    y = [LC[1, 0] + LC[1, 2], LC[1, 2], LC[1, 1] + LC[1, 2]]

    return x, y


# Origin
pi = [4, 7, 1]

# Translation
Dp = [3, 2, 1]

# Local coordinate system
LC1 = np.array([[1, 0, pi[0]], [0, 1, pi[1]], [0, 0, pi[2]]])

# Translation matrix
TM = np.array(
    [
        [1, 0, Dp[0]],
        [0, 1, Dp[1]],
        [0, 0, 1],
    ]
)

LC2 = TM @ LC1

x1, y1 = calc_x_y_for_lc(LC1)
fig = px.line(x=x1, y=y1)

x2, y2 = calc_x_y_for_lc(LC2)
fig.add_trace(px.line(x=x2, y=y2).data[0])

fig.update_traces(line_color="red", line_width=4)
fig.show()
