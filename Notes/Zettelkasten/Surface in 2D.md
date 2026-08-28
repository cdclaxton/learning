#Graphics 

A surface can be represented with two matrices so that $X_{i,j}$ and $Y_{i,j}$ correspond to point $i,j$:

$$
X = \begin{bmatrix}
x_{0,0} & x_{0,1} & \cdots & x_{0,N-1} \\
x_{1,0} & x_{1,1} & \cdots & x_{1,N-1} \\
\vdots & \vdots & & \vdots \\
x_{M-1, 0} & x_{M-1, 1} & \cdots & x_{M-1, N-1} \\
\end{bmatrix}
$$
and
$$
Y = \begin{bmatrix}
y_{0,0} & y_{0,1} & \cdots & y_{0,N-1} \\
y_{1,0} & y_{1,1} & \cdots & y_{1,N-1} \\
\vdots & \vdots & & \vdots \\
y_{M-1, 0} & y_{M-1, 1} & \cdots & y_{M-1, N-1} \\
\end{bmatrix}
$$
and the $2 \times 2$ matrix
$$
\begin{bmatrix}
x_{i,j} & x_{i,j+1} \\
x_{i+1,j} & x_{i+1, j+1} \\
\end{bmatrix}
$$
represents a patch.

**Array packing** converts the $X$ and $Y$ matrices into a single matrix:
$$
S = \begin{bmatrix}
x_{0,0} & x_{0,1} & \cdots & x_{0,N-1} & x_{1,0} & \cdots & x_{M-1,N-1} \\
y_{0,0} & y_{0,1} & \cdots & y_{0,N-1} & y_{1,0} & \cdots & y_{M-1,N-1} \\
1 & 1 & \cdots & 1 & 1 & \cdots & 1 \\
\end{bmatrix}
$$
This is composed of the rows of $X$ and $Y$. Each column corresponds to a single point on the surface.

Array packing is similar to the technique used to represent images in [[Neural network]]s

The surface can undergo [[Translation matrix]] 
