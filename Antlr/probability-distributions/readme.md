# Intepreter for discrete probability distributions

The code in this repo implements an interpreter to perform simple operations
on probability distributions.

An example program is:

```
a = {1: 0.2, 2: 0.8}
b = {3: 0.1, 4: 0.9}
c = {3: 0.5, 4: 0.5}
d = (a + b) | c
d
e = {4: 0.1, 6: 0.9} | d
e
```

and the output will be:

```

        █        |      █        Probability Distribution
        █ █    --+--  █ █              Calculator
        █ █ █    |    █ █ █

Program:
1 | a = {1: 0.2, 2: 0.8}
2 | b = {3: 0.1, 4: 0.9}
3 | c = {3: 0.5, 4: 0.5}
4 | d = (a + b) | c
5 | d
6 | e = {4: 0.1, 6: 0.9} | d
7 | e
8 | 

d = {4:0.020000, 5:0.260000, 6:0.720000}
e = {4:0.002000, 5:0.026000, 6:0.972000}
```

Variables must be composed of lowercase and upper case letters, e.g. `a`.

A probability distribution takes the form of `{ value: prob, [, value: prob]* }`.
Note that the sum of the `prob`s in a single distribution must sum to unity.

The operators `+`, `-`, `*` and `/` correspond to the usual arithmetic
operators, but in a distribution sense. Parentheses allow the usual precedence
rules to be overridden.

The operator `|` is an extension of a Noisy OR to a Noisy Max.

A variable on a line on its own prints the associated distribution.

To build and run the above program:

```
./build.sh
./probabilitydistributions programs/noisy-max.prob
```

The Antlr language is defined in `ProbabilityDistributions.g4`.