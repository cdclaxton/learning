#Graphics 

Projection matrix:
$$
P = \begin{bmatrix}
k_x & 0 & 0 & 0 \\
0 & k_y & 0 & 0 \\
0 & 0 & k_z & 0 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$
To project on to the:
- yz-axis: $k = \langle 0, 1, 1 \rangle$
- xz-axis: $k = \langle 1, 0, 1 \rangle$
- xy-axis: $k = \langle 1, 1, 0 \rangle$

Projection onto an arbitrary plane defined by the unit normal vector $n$ through the origin:
$$
\begin{align}
P &= I - (n \times n^\top) \\
  &= \begin{bmatrix}
  1 & 0 & 0 & 0 \\
  0 & 1 & 0 & 0 \\
  0 & 0 & 1 & 0 \\
  0 & 0 & 0 & 1 \\
\end{bmatrix} - 
  \begin{bmatrix}
  n_x \\ n_y \\ n_z \\ 0 \\
  \end{bmatrix} \times
  \begin{bmatrix}
  n_x & n_y & n_z & 0 \\
  \end{bmatrix}
\end{align}
$$
