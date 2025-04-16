/* Is there a path between vertices in an undirected graph?

   There are three connected components:

   a --- b --- c
         |
         d --- e

   f --- g --- h
   |           |
   |-----------|

   i --- j --- k --- l
         |     |
         m --- n --- o
*/

edge(a, b).
edge(b, c).
edge(b, d).
edge(d, e).

edge(f, g).
edge(g, h).
edge(f, h).

edge(i, j).
edge(j, k).
edge(k, l).
edge(j, m).
edge(m, n).
edge(k, n).
edge(n, o).

/* connected(A, B) satisfies if A and B are connected via an edge */
connected(A, B) :- edge(A, B) ; edge(B, A).

/* path(A, B) satisfies if there is a path from A to B */
path(A, B) :-
    walk(A, B, []).

walk(A, B, V) :-
    connected(A, X),
    not(member(X, V)),
    ( B = X ; walk(X, B, [A|V]) ).