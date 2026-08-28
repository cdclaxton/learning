#Graphics 

x-axis reflection matrix ($x' = x, y' = -y$):
$$
R = \begin{bmatrix}
1 & 0 & 0 \\
0 & -1 & 0 \\
0 & 0 & 0 \\
\end{bmatrix}
$$
y-axis reflection matrix ($x'=-x, y'=y$):
$$
R = \begin{bmatrix}
-1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 0 \\
\end{bmatrix}
$$
xy-axis reflection matrix ($x'=-x, y'=-y$)
$$
R = \begin{bmatrix}
-1 & 0 & 0 \\
0 & -1 & 0 \\
0 & 0 & 0 \\
\end{bmatrix}
$$

Reflection in 3D using the **Householder matrix** that reflects points about a plane (with normal vector $n = \langle n_x, n_y, n_z, 1 \rangle$) that passes through the origin:
$$
\begin{align}
H_n &= I - 2(n \times n^\top) \\
  &= \begin{bmatrix}
  1 & 0 & 0 & 0 \\
  0 & 1 & 0 & 0 \\
  0 & 0 & 1 & 0 \\
  0 & 0 & 0 & 1 \\
\end{bmatrix} - 2 
  \begin{bmatrix}
  n_x \\ n_y \\ n_z \\ 0 \\
  \end{bmatrix} \times
  \begin{bmatrix}
  n_x & n_y & n_z & 0 \\
  \end{bmatrix}
\end{align}
$$

Reflect a surface $S_1$:
$$
S_2 = H_n \times S_1
$$
