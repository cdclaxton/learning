# Prolog

Prolog = PROgramming in LOGic -- modelled on first order logic

Prolog is a computer language for solving problems that involve objects and relationships

Declarative language (whereas C is procedural)

Programming consists of:

- Declaring facts about objects and their relationships (declaration of a true state of affairs)
- Defining rules -- logic contains rules of inference
- Asking questions (a conjunction of goals to be satisfied using known clauses)

Modus ponens logic:

- p => q
- if proposition p is true, then conclude that q is true
- e.g. if it is raining, then the ground is wet. It is raining, therefore the ground is wet

Horn clause logic:

- Prolog uses a subset of First Order Logic called 'quantifier-free Horn clause logic'
- no existential or universal quantifiers
- any variable is implicitly assumed to be universally quantified
- `male(X).` means for all x, male(x), i.e. everything is male
- p [antecedent] => q [consequent] becomes `q :- p` in Prolog
- Horn clause => only one term in the consequent, i.e. before `:-`
- variables:
  - facts: universally quantified
    - `human(X).` => everything is human
  - queries: existentially quantified
    - `human(X).` => is there at least one thing that is human?
- deduction process involves matching terms in the goal against terms in the head of the rule and terms in the body of the rule against other terms
- matching process is called **unification**

Unification

- to unify, two terms must have the same arity
- basic terms unify as:
  - identical constants unify, e.g. chas and chas
  - a constant and a variable unify (side effect: variable takes value of constant)
  - two variables unify (e.g. X and Y)

Clauses = facts or rules

Prolog programs are built from terms:

- constants -- name specific objects or relationships
  - atoms -- letters and digits; signs (:-)
  - integers
- variables -- begin with a capital letter or underscore
- structure -- consists of a collection of other objects (components)
  - functor -- written before the opening round bracket
  - components -- enclosed in round brackets, comma separated
  - predicate -- functor of the structure

Comments -- `/* ... */`

Arity -- number of arguments of a compound term

## Installation

- Linux: sudo apt-get install swi-prolog
- Windows: download SWI-Prolog

## Running a file and exiting

```prolog
?- consult(<filename minus .pl>)
?- halt.
```

## Quick start

Put the following code into the text file `test.pl`:

```prolog
male(chris).
male(reuben).
female(ruth).
```

Start Prolog at the command line using: `prolog`

Read the database using: `?- consult(test).`

Ask a few questions:

```prolog
?- male(chris).
true.

?- female(sally).
false.
```

Quit by typing: `halt.`

## Facts

Names of all relationships and objects must begin with a lowercase letter

Format (note full-stop at the end): `<relationship>( <object1>, <object2>, ...).`

e.g.

```prolog
female(sally) /* Sally is female */
son_of(chris,reuben) /* Reuben is the son of Chris */
```

- Arguments -- names of objects
- Predicate -- name of the relationship, e.g. `son_of`
- Database -- collection of facts

## Questions

Begin with `?-`

Prolog searches through the database to look for facts that match the fact in question

Two facts match if their predicates are the same and the arguments are the same

Answer `false` implies that nothing matches the question (not provable)

## Variables

Begin with a capital letter

Variables can be instantiated (there is an object that the variable stands for) or not instantiated

Prolog searches through all of its facts to find an object that the variable could stand for

```prolog
in_sector(shell, oil_and_gas).
in_sector(gwr, rail).

?- in_sector(X,rail).
X = gwr.
```

press Enter --> Prolog stops searching for more answers

press ; --> Prolog will resume its search through the database

Anonymous variable:

- `_` symbol
- several anonymous variables in the same clause need not be given the same interpretation

## Conjunction

logical AND

symbol `,`

p,q is true iff p and q are true

backtracking --> repeated attempts to satisfy and re-satisfy goals in a conjunction

```prolog
boss_of(darren, chris).
boss_of(darren, david).

?- boss_of(X,chris), boss_of(X,david).
X = darren.
```

## Disjunction

logical or

symbol `;`

```prolog
outside_opening_hours(Time,Open,Close) :- Time < Open; Time > Close.

?- outside_opening_hours(15,8,21).
false.

?- outside_opening_hours(23,8,21).
true.
```

## Rules

A rule can be expressed much more succinctly than listing a set of facts

Rules can be used to state that a fact depends on a group of other facts

A rule is a general statement about objects and their relationships

Form: `H :- B.`

- note the full-stop
- `H` = head
- `B` = body
- `:-` = pronounced 'if'

```prolog
song(hosanna,e).
song(mighty_to_save,a).
song(blessed_be_your_name,a).

same_key(X,Y,K) :- song(X,K), song(Y,K), X \= Y.

?- same_key(X,Y,a).
X = mighty_to_save,
Y = blessed_be_your_name ;
X = blessed_be_your_name,
Y = mighty_to_save ;
false.
```

## Equality

`?- X = Y` <-- Prolog attempts to match X and Y. If X and Y unify, then true is returned

Equality is a built-in predicate

Rules for determining if X and Y are equal:

- if X is uninstantiated and Y is instantiated to any term, then X and Y are equal
- integers and atoms are always equal to themselves
- two structures are equal if they have the same functor and arguments

Predicate `\=` (not equal) succeeds if `X = Y` fails

`==` tests for literal equality without instantiating the variabes, e.g.

```prolog
?- a = X.
X = a.

?- a == X.
false.
```

## Arithmetic

`=`, `\=`, `<`, `>`, `=<`, `>=`

`+`, `-`, `*`, `/`, `mod`

```prolog
/* Guitarists in the Rolling Stones */
guitarist(keith_richards, 1962, 2011).
guitarist(brian_jones, 1962, 1969).
guitarist(mick_taylor, 1969, 1974).
guitarist(ronnie_wood, 1975, 2011).

/* Person was a guitarist in Year if:
   Person played guitar in years Start to End
   Year is between Start and End */
guitarist(Person,Year) :- guitarist(Person,Start,End), Year>=Start, Year=<End.

?- guitarist(X,1980).
X = keith_richards ;
X = ronnie_wood.
```

`is` operator:

- infix
- right-hand argument is a term that is interpreted as an arithmetic expression
- answer is matched with the left-hand argument to determine if the goal succeeds
- required for evaluating an arithmetic expression

```prolog
?- X is 3+2.
X = 5.
```

```prolog
multiply(X,Y,Z) :- Z is X*Y.

?- multiply(10,2,X).
X = 20.

?- multiply(10,X,20).
ERROR: is/2: Arguments are not sufficiently instantiated
```

```prolog
/* Power R = P^N */
power(_,0,1).
power(P,N,R) :- N>=0, N1 is N-1, power(P,N1,R1), R is R1*P.
```

## Recursion

Two components:

- base (non-recursive clause)
- recursion (calls itself)

## Data structures

### Trees

The structure `likes(chris,guitar)` can be written as a tree where each functor is a node and the components are the branches

### Lists

Ordered sequence of elements of any length

The elements can be constants, variables, structures

A list is either:

- empty `[]`
- structure with 2 components (head and tail)
- e.g. `[a], [a,b]`

Single element lists unify because they have the same arity

```prolog
?- [X] = [a].
X = a.

?- [a,b] = [X,Y].
X = a,
Y = b.
```

Lists can contain other lists and variables

Lists are manipulated by splitting them into a head and a tail

- Head -- first element of the list
- Tail -- a list containing every element except the first
- Prolog notation: `[H | T]`

```prolog
/* Split a list into a head and tail */
?- [a,b,c,d] = [H|T].
H = a,
T = [b, c, d].
```

```prolog
/* Get the first and second elements */
?- [a,b,c,d] = [F,S|T].
F = a,
S = b,
T = [c, d].
```

Lists can be used to represent strings and if a string is enclosed in double quotes, the string is represented as a list of integer codes that represent the ASCII characters

`append` -- predicate for joining two lists together

```prolog
?- append([a,b],[c,d],X).
X = [a, b, c, d].
```

The built-in predicate `append` can be used to find elements in a list

```prolog
?- append(X, [c,d], [a,b,c,d]).
X = [a, b] ;
```

`length` -- predicate returns the length of a list

```prolog
?- length([a,b,c,d],X).
X = 4.
```

Alternative implementation of the built-in length predicate:

```prolog
find_length([], 0).
find_length([H|T],N) :- find_length(T,N1), N is N1+1.

?- find_length([a,b,c],X).
X = 3.

?- find_length([],X).
X = 0.
```

List membership:

```prolog
/* List membership: member(X,L) succeeds if X is in list L */
member(X,[Y|_]) :- X = Y.		/* Boundary condition */
member(X,[_|Y]) :- member(X,Y).	/* Recursive case */

?- member(cat,[dog,cat,fox]).
true ;

?- member(X,[a,b,c]).
X = a ;
X = b ;
X = c ;
```

```prolog
/* Not a member
   not_member(X,L) succeeds if X is not a member of list L */

not_member(X,[]).
not_member(X,[H|T]) :- X \= H, not_member(X,T).

?- not_member(cat, [dog,fox]).
true .

?- not_member(dog, [dog,fox]).
false.
```

```prolog
/* accumulate(X,N) succeeds if N is the sum of values in X */
accumulate([],0).
accumulate([H|T],N) :- accumulate(T,N1), N is N1+H.

?- accumulate([1,2,3],X).
X = 6.
```

```prolog
/* inner_product(X,Y,N) succeeds if the inner product of
   lists X and Y is N */
inner_product([], [], 0).
inner_product([H1|T1],[H2|T2],N) :- inner_product(T1,T2,N2), N is N2+(H1*H2).

?- inner_product([1,2],[3,4],X).
X = 11.
```

Add two lists together:

```prolog
list_sum([],[],[]).
list_sum([H1|T1], [H2|T2], [H|L3]) :-
	list_sum(T1,T2,L3),
	H is H1+H2.

?- list_sum([1,2,3],[10,20,30],X).
X = [11, 22, 33].
```

```prolog
/* max(L,A,M) succeeds if M is the largest element of the list
   greater than A */
max([],A,A).
max([H|T],A,M) :- H >= A, max(T,H,M).
max([H|T],A,M) :- H < A, max(T,A,M).
get_head([H|_],H).
maximum(L,M) :- get_head(L,H), max(L,H,M).
→
8 ?- maximum([1,2,0],X).
X = 2.
```

```prolog
/* Example of a partial map
   Predicate evens(X,L) succeeds if L contains just the even numbers in X. */
evens([],[]).
evens([X|T],[X|L]) :- 0 is X mod 2, evens(T,L).
evens([X|T],L) :- 1 is X mod 2, evens(T,L).
→
1 ?- evens([1,2,3,4,5],X).
X = [2, 4].
```

```prolog
/* Example of a partial map
   Program removes specified names */
name(dave).
name(george).

censor([],[]).
censor([H|T], L) :- name(H), censor(T,L).
censor([H|T], [H|L]) :- censor(T,L).
→
1 ?- censor([hello,dave,and,chris],X).
X = [hello, and, chris].
```

Walk through a list, printing each element:

```prolog
print_element(X) :-
	write('Element: '), write(X), nl.

print_elements([]).
print_elements([H|T]) :-
	print_element(H),
	print_elements(T).

?- print_elements([1,2,3]).
Element: 1
Element: 2
Element: 3
true.
```

## Graphs

Directed Acyclic Graphs (DAGs) can be represented in Prolog

```prolog
/* Database of arcs */
arc(a,b).
arc(a,d).
arc(b,d).
arc(b,c).
arc(d,e).

/* Predicate path(A,B) succeeds if there is a path from node
   A to node B */
path(A,B) :- arc(A,B).
path(A,B) :- arc(A,X), path(X,B).

?- path(c,e).
false.

?- path(a,c).
true .
```

## Cut

Tells Prolog which previous choices it need not consider again when it backtracks through a chain of satisfied goals

Uses of cuts:

- program will operate faster because it will not waste time attempting to satisfy goals that will never contribute to a solution
- program may occupy less memory if backtracking points aren't required for later examination

Represented as the symbol `!`

When a cut is encountered as a goal, the system is committed to all choices made since the parent goal was invoked. All other alternatives are discarded.

Consider the conjunction of goals:

`foo :- a, b, c ! d, e, f`

Prolog will backtrack among goals a, b and c until the success of c causes the fence to be crossed. Then backtracking will only occur among d, e, and f. However, if goal d fails, no attempt will be made to re-satisfy goal c, i.e. the conjunction of goals will fail and the goal foo will fail.

Common uses for cut:

- "if you get to here, you have picked the correct rule for this goal"
- "if you get to here, you should stop trying to satisfy this goal"
- "if you get to here, you have found the only solution to this problem, and there is no point looking for alternatives"

```prolog
male(chris).
male(fred).
female(katherine).

find_male(X) :- male(X), !.

?- find_male(X).
X = chris.
```

## Input and output

When characters between double quotes are printed in Prolog, it appears as ASCII codes.

```prolog
event(1511, "Luther visits Rome").
event(1521, "Henry VIII is made Defender of the Faith").

?- event(1511,X).
X = "Luther visits Rome".
```

`write` -- built-in predicate

- if `X` is instantiated, the goal `write(X)` will cause the term to be printed
- if `X` is not instantiated, a uniquely numbered variable will be printed

`nl` -- built-in predicate and means 'new line'

`tab(X)` -- built-in predicate to print a number (X, integer) of blank spaces

```prolog
?- write('Hello Chris'), write('!').
Hello Chris!
true.

?- write('Hello Chris'), nl, write('!').
Hello Chris
!
true.

?- tab(10), write('Hello Chris'), nl, write('!').
          Hello Chris
!
true.
```

`read` -- built-in predicate to read a term (where the term must be followed by a dot)

```prolog
?- read(X).
|: 1234.

X = 1234.
```

```prolog
event(1511, "Luther visits Rome").
event(1521, "Henry VIII is made Defender of the Faith").

quest :- write('Enter date: '), read(D), event(D,S), write(S).

?- quest.
Enter date: 1521.
Henry VIII is made Defender of the Faith
true.
```

## Built-in predicates

`consult(X)` -- clauses in the file augment those in the database, where the argument is the name of the file the clauses are to be taken from. The clauses are added to the end of the database.

`reconsult(X)` -- clauses read in supersede all existing clauses for the same predicate (useful for correcting programming mistakes).

List notation can be used to consult and reconsult files, e.g. [file1, file2, file3]

`true` -- goal always succeeds

`false` -- goal always fails

`var(X)` -- succeeds if X is currently uninstantiated

`nonvar(X)` -- succeeds if X is instantiated

`atom(X)` -- succeeds if X stands for a Prolog term

`integer(X)` -- succeeds if X stands for an integer

`atomic(X)` -- succeeds if X stands for an integer or an atom

`listing(A)` -- causes all predicates with atom A to be printed

`display(X is 5+9)` -- shows the real constitution of expressions

```prolog
event(1511, "Luther visits Rome").
event(1521, "Henry VIII is made Defender of the Faith").

quest :- write('Enter date: '), read(D), event(D,S), write(S).

?- listing(event).
event(1511, "Luther visits Rome").
event(1521, "Henry VIII is made Defender of the Faith").
```

`asserta(Z)` -- adds a clause to the beginning of the database, where Z is instantiated

`assertz(Z)` -- adds a clause to the end of the database

```prolog
?- asserta(male(chris)).
true.

?- male(X).
X = chris.
```

`retract(X)` -- remove clause from the database

```prolog
?- asserta(male(chris)).
true.

?- asserta(male(james)).
true.

?- listing(male).
:- dynamic male/1.

male(james).
male(chris).

true.

?- retract(male(chris)).
true.

?- listing(male).
:- dynamic male/1.

male(james).

true.
```

## Examples

Dynamically make changes to the database:

```prolog
add_book(BookName) :-
	write('Adding book: '), write(BookName),
	asserta(book(BookName)).
```

Simple state machine:

```prolog
update(OldState, NewState) :-
	OldState == 0,
	NewState is 1.

update(OldState, NewState) :-
	OldState == 1,
	NewState is 0.
```

Group points based on an index (a non-overlapping grouping):

```prolog
/* Define a set of points: point(name, time) predicate */
point('A',1).
point('B',2).
point('C',10).
point('D',14).
point('E',15).
point('F',16).

/* Rules to group points */
group(Start,End,GroupName) :-
	point(PointName,T),
	T >= Start, T =< End,
	asserta(group_point(GroupName,PointName)),
	write('Added point '), write(PointName),
	write(' to Group: '), write(GroupName).

/* Group points by the point index */
group_by_index(GroupIndex) :-
	Start is (GroupIndex*4 + 1),
	End is (Start + 3),
	group(Start, End, GroupIndex).

/* Remove all of the groups */
clear_all_groups :- retractall(group_point(_,_)).

/* Automatically generate the groups of points */
gen_groups(Start,Stop) :-
	between(Start, Stop, GroupIndex),
	group_by_index(GroupIndex).

?- gen_groups(0,5).
Added point A to Group: 0
true ;
Added point B to Group: 0
true ;
Added point C to Group: 2
true ;
Added point D to Group: 3
true ;
Added point E to Group: 3
true ;
Added point F to Group: 3
true ;
false.
```
