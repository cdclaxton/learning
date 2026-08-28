#Graphics 

Given a set of $N$ control points and a blending weight $B_i(u)$:
$$
p(u) = \sum_{i=0}^{N-1} B_i(u) p_i
$$
where $u \in [0,1]$ and $B_i(u)$ is the Bernstein polynomial:
$$
B_i(u) = {n \choose i} u^i (1-u)^{N-i} 
$$
To make the path closed, simply append the first point to the end of the control points.