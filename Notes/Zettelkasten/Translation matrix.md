#Graphics 

- Change in position of an object (size and orientation remain the same)

Translation in 2D:
- Translation matrix composed of column vectors $[v_x, v_y, D_p]$ were $v_x$ and $v_y$ are unit vectors
- $D_p$ is a translation point where  $D_x$ is the x-axis translation and $D_y$ is the y-axis translation
$$
TM = 
\begin{bmatrix}
1 & 0 & D_x \\
0 & 1 & D_y \\
0 & 0 & 1 \\
\end{bmatrix}
$$
- Translation of a local coordinate system
$$
\begin{align}
LC_2 &= TM \times LC_1 \\
 &= \begin{bmatrix}
1 & 0 & D_x \\
0 & 1 & D_y \\
0 & 0 & 1 \\
\end{bmatrix} \times
\begin{bmatrix}
1 & 0 & x_i \\
0 & 1 & y_i \\
0 & 0 & 1
\end{bmatrix} \\
 &= 
\begin{bmatrix}
1 & 0 & x_i + D_x \\
0 & 1 & y_i + D_y \\
0 & 0 & 1 \\
\end{bmatrix}
\end{align}
$$
- Translation of a curve or surface in 2D represented as a matrix $C_1$ of $N$ points:
$$
\begin{align}
C_2 &= TM \times C_1 \\
  &= \begin{bmatrix}
1 & 0 & D_x \\
0 & 1 & D_y \\
0 & 0 & 1 \\
\end{bmatrix} \times
\begin{bmatrix}
x_0 & x_1 & \cdots & x_{N-1} \\
y_0 & y_1 & \cdots & y_{N-1} \\
1 & 1 & \cdots & 1 \\
\end{bmatrix}
\end{align}
$$
Translation in 3D:
$$
TM = 
\begin{bmatrix}
1 & 0 & 0 & D_x \\
0 & 1 & 0 & D_y \\
0 & 0 & 1 & D_z \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$
