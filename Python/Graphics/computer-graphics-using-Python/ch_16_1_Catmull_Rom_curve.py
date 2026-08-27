import math
import numpy as np
import plotly.express as px

# Random control points
Qk = np.random.rand(7,3)

# To make a closed curve:
Qk = np.concatenate((Qk, 
                     Qk[0,:].reshape(1,-1),
                     Qk[1,:].reshape(1,-1),
                     Qk[2,:].reshape(1,-1)))

# Calculate the curve
u = np.transpose(np.linspace(0,1,50).reshape(1,-1))
Uk = np.concatenate((u**3, u**2, u, np.ones(np.shape(u))), axis=1)
Mk = 1/2 * np.array([
    [-1, 3, -3, 1],
    [2, -5, 4, -1],
    [-1, 0, 1, 0],
    [0, 2, 0, 0],
])
pu = np.zeros((len(u) * (len(Qk) - len(Mk) + 1), 3))
for i in range(len(Qk) - len(Mk) + 1):
    Qk_stage = Qk[i:i+len(Mk),:]
    pu[len(u)*i:len(u)*(i+1), 0:3] = Uk @ Mk @ Qk_stage

# Draw the control points
fig = px.line_3d(x=Qk[:,0], y=Qk[:,1], z=Qk[:,2],
                 line_dash=None,
                 markers=True, 
                 color_discrete_sequence=['red'])

# Draw the Catmull-Rom curve
fig.add_trace(px.line_3d(
    x=pu[:,0], y=pu[:,1], z=pu[:,2],
    color_discrete_sequence=['darkblue']).data[0])

fig.show()