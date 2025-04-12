/* Add a number A to each list element in [H1|T1] */
add([], _, []).
add([H1|T1], A, [H2|T2]) :- add(T1, A, T2), H2 is A+H1.

times([], _, []).
times([H1|T1], A, [H2|T2]) :- times(T1, A, T2), H2 is A*H1.

/* Add two lists together */
sum([], [], []).
sum([H1|T1], [H2|T2], [H3|T3]) :- sum(T1, T2, T3), H3 is H1+H2.

/* Filter a list to retain even numbers */
evens([], []).
evens([H1|T1], [H1|T2]) :- 0 is H1 mod 2, evens(T1,T2).
evens([H1|T1], L) :- 1 is H1 mod 2, evens(T1,L).

/* List of numbers from 1 to M in reverse */
numbersInRange(0, []) :- !.
numbersInRange(M, [H|T]) :- H is M, N is M-1, numbersInRange(N, T). 

/* Creates a list of numbers from 1 to M and doubles each value */
doubled(M, Result) :-
    numbersInRange(M, Numbers),
    times(Numbers, 2, Result).

/* Given a list of values V and their probabilities P, find the value that 
   maximises the probability 

   argMax(['a', 'b', 'c'], [0.7, 0.9, 0.1], V, P).   
*/
argMaxHelper([], [], PartialMax, PartialMax, PartialV, PartialV).
argMaxHelper([V1|V2], [P1|P2], PartialMax, FinalMax, _, FinalV) :- 
    P1>PartialMax, argMaxHelper(V2, P2, P1, FinalMax, V1, FinalV).
argMaxHelper([_|V2], [P1|P2], PartialMax, FinalMax, PartialV, FinalV) :- 
    P1=<PartialMax, argMaxHelper(V2, P2, PartialMax, FinalMax, PartialV, FinalV).
argMax(V, P, PMax, VMax) :- argMaxHelper(V, P, 0, PMax, 0, VMax).
