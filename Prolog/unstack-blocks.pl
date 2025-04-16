/* Unstack blocks

   Determine the sequence to remove the blocks.

   +-----------+-----+
   |     a     |  b  |
   +--------+--+-----+
   |    c   |    d   |
   +----+---+---+----+
   | e  |   f   | g  |
   +----+-------+----+
   |    floor        |
   +-----------------+

   To execute: clean.
*/

/* dynamic directive is required to assert and retract facts defined in a file */
:- dynamic(on/2).

on(a,c).
on(a,d).
on(b,d).
on(c,e).
on(c,f).
on(d,f).
on(d,g).
on(e,floor).
on(f,floor).
on(g,floor).

clean :-
    on(A, _), 
    \+on(_, A),
    write('Remove '), write(A), nl,
    retractall(on(A, _)),
    clean.

clean.
