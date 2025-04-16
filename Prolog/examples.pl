/* Prolog examples 
   Resource used: https://www2.cs.arizona.edu/classes/cs372/fall06/prolog.sli.pdf
*/

/* Print the numbers from 1 to N 
   ?- printN(3).
   1
   2
   3
   true .
*/
printN(0).
printN(N) :- N > 0, M is N - 1, printN(M), writeln(N).

/* Sum integers from 1 to N 
   ?- sumN(4, X).
   X = 10 .
*/
sumN(0, 0).
sumN(N, Sum) :- N > 0, M is N - 1, sumN(M, PartialSum), Sum is N + PartialSum.

/* Is a number odd?
   ?- odd(2).
   false.

   ?- odd(1).
   true.
*/
odd(N) :- N mod 2 =:= 1.

/* Is a number odd? This recursive approach can generate the odd numbers
   ?- odd2(X).
   X = 1 ;
   X = 3 ;
   X = 5 ;
   X = 7 
*/
odd2(1).
odd2(N) :- odd2(M), N is M + 2.

/* Has vowel 
   ?- has_vowel('abc').
   true .
*/
has_vowel(Text) :- 
    atom_chars(Text, L), member(Char, L), member(Char, [a, e, i, o, u]).

/* Starts with 
   ?- starts_with([a,b,c], X).
   X = [a] .
*/
starts_with(L, Prefix) :- append(Prefix, _, L), length(Prefix, 1).

/* Last element of a list 
   ?- last1([a,b,c], X).
   X = c.

   ?- last2([a,b,c], X).
   X = c .
*/
last1(List, Element) :- List = [Element|_], length(List, 1).
last1(List, Element) :- List = [_|T], last(T, Element).

last2([X], X).
last2([_|T], X) :- last2(T, X).

/* Length of a list (similar to the in-built length/2)
   ?- len([], X).
   X = 0.

   ?- len([a], X).
   X = 1.

   ?- len([a, b, c], X).
   X = 3.
*/
len([], 0).
len([_|T], Length) :- len(T, N), Length is N + 1.

/* Predicate allsame(L) is satisfied if all elements have the same value
   ?- allsame([a, a]).
   true .

   ?- allsame([a, b]).
   false.
*/
tailChecker([X], X).
tailChecker([H|T], H) :- tailChecker(T, H).
allsame(List) :- tailChecker(List, _).

/* Predicate listeq(L1, L2) is satisfied if the lists L1 and L2 hold the 
   same sequence of values
   ?- listeq([a,b], [a,b]).
   true.

   ?- listeq([a,b], [a,c]).
   false.
*/
listeq([], []).
listeq([H1|T1], [H2|T2]) :- H1 = H2, listeq(T1, T2).

/* Maximum of two elements
   ?- max(2,1,X).
   X = 2.

   ?- max(2,3,X).
   X = 3.
*/
max(X, Y, MaxValue) :- X > Y, X = MaxValue, ! ; Y = MaxValue.

/* All values in the list are positive (using the 'cut-fail' idiom)
   ?- all_positive([1,2,3]).
   true.

   ?- all_positive([1,-2,3]).
   false.
*/
all_positive(List) :- member(X, List), X =< 0, !, fail.
all_positive(_).

/* Unification of lists of predicates 
   [food(B, green), food(carrot, O)] = [food(brocolli, G), food(C, orange)].
   B = brocolli,
   O = orange,
   G = green,
   C = carrot.
*/
food(brocolli, green).
food(carrot, orange).
food(peas, green).

/* Pairs 
   ?- pairs([1,2,3,4], L, R).
   L = 1,
   R = 2 ;
   L = 2,
   R = 3 ;
   L = 3,
   R = 4 ;
*/
pairs([Left, Right | _], Left, Right).
pairs([_ | Rest], Left, Right) :- pairs(Rest, Left, Right).

/* Two elements are next to each other 
   ?- next_to(2,3,[1,2,3,4]).
   true .

   ?- next_to(1,3,[1,2,3,4]).
   false.
*/
next_to(X, Y, List) :- pairs(List, X, Y).
next_to(X, Y, List) :- pairs(List, Y, X).