#Graphics 

- Extends Cartesian coordinate system
- Adds one more dimension, e.g. a 2D point $\langle x,y \rangle$ becomes $\langle x,y,1 \rangle$
- A 3D point $\langle x,y,z \rangle$ becomes $\langle x,y,z,1 \rangle$
- Vector $v$ has the additional dimension set to zero, e.g. $\langle \Delta x, \Delta y,0  \rangle$ for a 2D vector and $\langle \Delta x, \Delta y, \Delta z, 0 \rangle$ for a 3D vector

**Global coordinate system**
- Immutable, overarching coordinate system

**Local homogeneous coordinate system**
- Have defined positions and orientations relative to the global coordinate system
- 2D local coordinate system:
$$
LC = 
\begin{bmatrix}
1 & 0 & x_i \\
0 & 1 & y_i \\
0 & 0 & 1
\end{bmatrix}
$$

- Composed of the columns $[ v_x, v_y, p_i]$ where $v_x$ and $v_y$ are unit vectors and $p_i = \langle x_i, y_i, 1 \rangle$ is the origin
- 3D local coordinate system:
$$
LC = 
\begin{bmatrix}
1 & 0 & 0 & x_i \\
0 & 1 & 0 & y_i \\
0 & 0 & 1 & z_i \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$
- Composed of the columns $[v_x, v_y, v_z, p_i]$ where $p_i$ is the origin