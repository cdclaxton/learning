/* Simple interpreter 

   run.
   set(10).
   add(5).
   print.
*/

init :-
    retractall(value(_)),  % remove value
    assert(value(0)).      % set value to 0

do(set(V)) :-
    retract(value(_)),     % remove value
    assert(value(V)).      % set value to V

do(print) :- 
    value(V), write(V), nl.

do(exit).

do(add(X)) :-
    value(V), T is V+X, do(set(T)).

do(sub(X)) :-
    value(V), T is V-X, do(set(T)).

do(mul(X)) :-
    value(V), T is V*X, do(set(T)).

do(div(X)) :-
    value(V), T is V/X, do(set(T)).

run :-
    init,
    repeat, write('> '), read(X), do(X), X = exit.
