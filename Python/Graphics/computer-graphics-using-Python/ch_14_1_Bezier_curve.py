import math
import numpy as np
import plotly.express as px

# Define a series of random points
n = 5
Qk = np.random.rand(n,3)

# For a closed loop, append the first point as the last point
Qk = np.concatenate((Qk, Qk[0,:].reshape(1,-1)))

# Calculate the curve
u = np.transpose(np.linspace(0,1,50).reshape(1,-1))
Bi = np.zeros((len(u), len(Qk)))
for i in range(len(Qk)):
    b = math.comb(n,i) * u**i * (1-u) ** (n-i)
    Bi[:,i] = b[:,0]

pu = Bi @ Qk

# Draw the control points
fig = px.line_3d(x=Qk[:,0], y=Qk[:,1], z=Qk[:,2],
                 markers=True, 
                 color_discrete_sequence=['red'])

# Draw the Bezier curve
fig.add_trace(px.line_3d(
    x=pu[:,0], y=pu[:,1], z=pu[:,2],
    color_discrete_sequence=['darkblue']).data[0])

fig.show()