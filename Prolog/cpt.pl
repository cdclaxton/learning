/* Retrieve row from Conditional Probability Table (CPT) */

/* The network is A --> B

     A |  B
    ---|---
     0 | p0
     1 | p1
*/

cpt1(A, B) :- \+ A, B = p0 ; A, B = p1.


/* There is a table for node A that depends on B and C.
   
    B  C  |  A
   -------|----
    0  0  | p0
    0  1  | p1
    1  0  | p2
    1  1  | p3
*/

cpt2(B, C, A) :- 
    \+ B, \+ C, A = p0 ; 
    \+ B, C, A = p1 ; 
    B, \+ C, A = p2 ; 
    B, C, A = p3.

/* Marginal probability */
marginal2(PB, PC, PA, P0, P1, P2, P3) :-
    PA is P0 * (1-PB) * (1-PC) +
        P1 * (1-PB) * PC +
        P2 * PB * (1-PC) +
        P3 * PB * PC.