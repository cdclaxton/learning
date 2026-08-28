#Graphics 

Rotation is one of the [[Rigid transformations]] (preserves distances and angles within an object)

Rotation matrix (around origin) in 2D:
$$
RM = \begin{bmatrix}
\cos \theta & -\sin \theta & 0 \\
\sin \theta & \cos \theta & 0 \\
0 & 0 & 1 \\
\end{bmatrix}
$$
Positive rotation is anti-clockwise

Rotation of a curve: $C_2 = TM \times C_1$

Rotation about a pivot point $D = \langle D_x, D_y, 1 \rangle$ using a **Total transformation matrix**:
$$
TTM = 
\begin{bmatrix}
1 & 0 & D_x \\
0 & 1 & D_y \\
0 & 0 & 1 \\
\end{bmatrix}
\times
\begin{bmatrix}
\cos \theta & - \sin \theta & 0 \\
\sin \theta & \cos \theta & 0 \\
0 & 0 & 1 \\
\end{bmatrix}
\times
\begin{bmatrix}
1 & 0 & D_x \\
0 & 1 & D_y \\
0 & 0 & 1 \\
\end{bmatrix}^{-1}
$$
Rotation in 3D using the **right-hand rule**:
x-axis rotation in 3D:
$$
R_x(\theta) = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & \cos \theta & -\sin \theta & 0 \\
0 & \sin \theta & \cos \theta & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$
y-axis rotation in 3D:
$$
R_x(\theta) = \begin{bmatrix}
\cos \theta & 0 & \sin \theta & 0 \\
0 & 1 & 0 & 0 \\
-\sin \theta & 0 & \cos \theta & 0 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$
z-axis rotation in 3D:
$$
R_z(\theta) = \begin{bmatrix}
\cos \theta & -\sin \theta & 0 & 0 \\
\sin \theta & \cos \theta & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

Rotation of a point $p$ by $\theta$ around the axis given by the vector $e$:
$$
e_1 = e \sin(\theta / 2)
$$
$$
F = \cos(\theta/2)
$$
$$
p' = p_1 + 2F (e_1 \otimes p) + 2(e_1 \otimes (e_1 \otimes p_1))
$$
where $\otimes$ is the vector cross product.