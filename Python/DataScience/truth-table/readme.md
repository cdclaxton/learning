# Build a truth table from a Boolean equation

## Example 1

Suppose that there is a single input denoted $A$. The truth table showing $A$ and its inverse ($\bar{A}$) is shown below.

| $A$ | $T_0$ | $T_1$ |
|-----|-------|-------|
| 0   | 0     | 1     |
| 1   | 1     | 0     |

Equations:
* $T_0 = A$
* $T_1 = \bar{A}$


## Example 2

There are two inputs, $A$ and $B$, and two 'bands' denoted Low and High. The logic used for the bands is expressed in the table:

| Band  | Input |
|-------|-------|
| Low   | A     |
| High  | B     |

It is assumed that the presence of $B$ irrespective of the state of $A$ dominates. The Low band is used if $D_{low}$ is true and the High band is used if $D_{high}$ is true. The truth table capturing this logic is shown below.

| $B$ | $A$ | $T_{low}$ | $T_{high}$ |
|-----|-----|-----------|------------|
| 0   | 0   | 0         | 0          |
| 0   | 1   | 1         | 0          |
| 1   | 0   | 0         | 1          |
| 1   | 1   | 0         | 1          |
| 1   | 1   | 0         | 1          |

Equations:
* $T_{low} = A \bar{B}$
* $T_{high} = B$

## Example 3

Building on the previous example, assume that the Low band should be triggered if either $A$ or $B$ are present. The High band should only be triggered if $C$ is present.

| Band | Input |
|------|-------|
| Low  | A, B  |
| High | C     |

The truth table where $C$ dominates is shown below.

| $C$ | $B$ | $A$ | $T_{low}$ | $T_{high}$ |
|-----|-----|-----|-----------|------------|
| 0   | 0   | 0   | 0         | 0          |
| 0   | 0   | 1   | 1         | 0          |
| 0   | 1   | 0   | 1         | 0          |
| 0   | 1   | 1   | 1         | 0          |
| 1   | 0   | 0   | 0         | 1          |
| 1   | 0   | 1   | 0         | 1          |
| 1   | 1   | 0   | 0         | 1          |
| 1   | 1   | 1   | 0         | 1          |

Equations:
* $T_{low} = (A + B)\bar{C}$
* $T_{high} = C$

## Example 4

In this example, the High band is triggered by either $C$ or $D$ being true and they each dominate $A$ and $B$.

| Band | Input |
|------|-------|
| Low  | A, B  |
| High | C, D  |

| $D$ | $C$ | $B$ | $A$ | $T_{low}$ | $T_{high}$ |
|-----|-----|-----|-----|-----------|------------|
| 0   | 0   | 0   | 0   | 0         | 0          |
| 0   | 0   | 0   | 1   | 1         | 0          |
| 0   | 0   | 1   | 0   | 1         | 0          |
| 0   | 0   | 1   | 1   | 1         | 0          |
| 0   | 1   | 0   | 0   | 0         | 1          |
| 0   | 1   | 0   | 1   | 0         | 1          |
| 0   | 1   | 1   | 0   | 0         | 1          |
| 0   | 1   | 1   | 1   | 0         | 1          |
| 1   | 0   | 0   | 0   | 0         | 1          |
| 1   | 0   | 0   | 1   | 0         | 1          |
| 1   | 0   | 1   | 0   | 0         | 1          |
| 1   | 0   | 1   | 1   | 0         | 1          |
| 1   | 1   | 0   | 0   | 0         | 1          |
| 1   | 1   | 0   | 1   | 0         | 1          |
| 1   | 1   | 1   | 0   | 0         | 1          |
| 1   | 1   | 1   | 1   | 0         | 1          |

Equations:
* $T_{low} = (A + B) \overline{(C + D)} = (A + B) \bar{C} \bar{D}$
* $T_{high} = C + D$

## Example 5

Suppose there are now three bands denoted Low, Medium and High.

| Band   | Input |
|--------|-------|
| Low    | A     |
| Medium | B     |
| High   | C     |

It is assumed that the presence of $B$ dominates $A$ and similarly for $C$ over $B$ and $A$.

| $C$ | $B$ | $A$ | $T_{low}$ | $T_{medium}$ | $T_{high}$ |
|-----|-----|-----|-----------|--------------|------------|
| 0   | 0   | 0   | 0         | 0            | 0          |
| 0   | 0   | 1   | 1         | 0            | 0          |
| 0   | 1   | 0   | 0         | 1            | 0          |
| 0   | 1   | 1   | 0         | 1            | 0          |
| 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0         | 0            | 1          |

Equations:
* $T_{low} = A \overline{(B + C)} = A \bar{B} \bar{C}$
* $T_{medium} = B \bar{C}$
* $T_{high} = C$

## Example 6

Building on the previous example, each band now has two inputs on which it depends.

| Band   | Input |
|--------|-------|
| Low    | A, B  |
| Medium | C, D  |
| High   | E, F  |

| $F$ | $E$ | $D$ | $C$ | $B$ | $A$ | $T_{low}$ | $T_{medium}$ | $T_{high}$ |
|-----|-----|-----|-----|-----|-----|-----------|--------------|------------|
| 0   | 0   | 0   | 0   | 0   | 0   | 0         | 0            | 0          |
| 0   | 0   | 0   | 0   | 0   | 1   | 1         | 0            | 0          |
| 0   | 0   | 0   | 0   | 1   | 0   | 1         | 0            | 0          |
| 0   | 0   | 0   | 0   | 1   | 1   | 1         | 0            | 0          |
| 0   | 0   | 0   | 1   | 0   | 0   | 0         | 1            | 0          |
| 0   | 0   | 0   | 1   | 0   | 1   | 0         | 1            | 0          |
| 0   | 0   | 0   | 1   | 1   | 0   | 0         | 1            | 0          |
| 0   | 0   | 0   | 1   | 1   | 1   | 0         | 1            | 0          |
| 0   | 0   | 1   | 0   | 0   | 0   | 0         | 1            | 0          |
| 0   | 0   | 1   | 0   | 0   | 1   | 0         | 1            | 0          |
| 0   | 0   | 1   | 0   | 1   | 0   | 0         | 1            | 0          |
| 0   | 0   | 1   | 0   | 1   | 1   | 0         | 1            | 0          |
| 0   | 0   | 1   | 1   | 0   | 0   | 0         | 1            | 0          |
| 0   | 0   | 1   | 1   | 0   | 1   | 0         | 1            | 0          |
| 0   | 0   | 1   | 1   | 1   | 0   | 0         | 1            | 0          |
| 0   | 0   | 1   | 1   | 1   | 1   | 0         | 1            | 0          |
| 0   | 1   | 0   | 0   | 0   | 0   | 0         | 0            | 1          |
| 0   | 1   | 0   | 0   | 0   | 1   | 0         | 0            | 1          |
| 0   | 1   | 0   | 0   | 1   | 0   | 0         | 0            | 1          |
| 0   | 1   | 0   | 0   | 1   | 1   | 0         | 0            | 1          |
| 0   | 1   | 0   | 1   | 0   | 0   | 0         | 0            | 1          |
| 0   | 1   | 0   | 1   | 0   | 1   | 0         | 0            | 1          |
| 0   | 1   | 0   | 1   | 1   | 0   | 0         | 0            | 1          |
| 0   | 1   | 0   | 1   | 1   | 1   | 0         | 0            | 1          |
| 0   | 1   | 1   | 0   | 0   | 0   | 0         | 0            | 1          |
| 0   | 1   | 1   | 0   | 0   | 1   | 0         | 0            | 1          |
| 0   | 1   | 1   | 0   | 1   | 0   | 0         | 0            | 1          |
| 0   | 1   | 1   | 0   | 1   | 1   | 0         | 0            | 1          |
| 0   | 1   | 1   | 1   | 0   | 0   | 0         | 0            | 1          |
| 0   | 1   | 1   | 1   | 0   | 1   | 0         | 0            | 1          |
| 0   | 1   | 1   | 1   | 1   | 0   | 0         | 0            | 1          |
| 0   | 1   | 1   | 1   | 1   | 1   | 0         | 0            | 1          |
| 1   | 0   | 0   | 0   | 0   | 0   | 0         | 0            | 1          |
| 1   | 0   | 0   | 0   | 0   | 1   | 0         | 0            | 1          |
| 1   | 0   | 0   | 0   | 1   | 0   | 0         | 0            | 1          |
| 1   | 0   | 0   | 0   | 1   | 1   | 0         | 0            | 1          |
| 1   | 0   | 0   | 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 0   | 0   | 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 0   | 0   | 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 0   | 0   | 1   | 1   | 1   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0   | 0   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0   | 0   | 1   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0   | 1   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0   | 1   | 1   | 0         | 0            | 1          |
| 1   | 0   | 1   | 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 0   | 1   | 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 1   | 1   | 1   | 0         | 0            | 1          |
| 1   | 1   | 0   | 0   | 0   | 0   | 0         | 0            | 1          |
| 1   | 1   | 0   | 0   | 0   | 1   | 0         | 0            | 1          |
| 1   | 1   | 0   | 0   | 1   | 0   | 0         | 0            | 1          |
| 1   | 1   | 0   | 0   | 1   | 1   | 0         | 0            | 1          |
| 1   | 1   | 0   | 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 1   | 0   | 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 1   | 0   | 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 1   | 0   | 1   | 1   | 1   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0   | 0   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0   | 0   | 1   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0   | 1   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0   | 1   | 1   | 0         | 0            | 1          |
| 1   | 1   | 1   | 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 1   | 1   | 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 1   | 1   | 1   | 0         | 0            | 1          |

Equations:
* $T_{low} = (A + B) \overline{(C + D + E + F)} = (A + B) \bar{C} \bar{D} \bar{E} \bar{F}$
* $T_{medium} = (C + D) \overline{(E + F)} = (C + D) \bar{E} \bar{F}$
* $T_{high} = E + F$

## Example 7

Suppose the Low band is as before, i.e. composed of inputs that are relevant. However, the High band is described in terms of aggravating factors.

It is noticeable how just the presence of the aggravating factor $C$ does not cause $T_{low}$ or $T_{high}$ to be true.

| Band | Input                                      |
|------|--------------------------------------------|
| Low  | A, B                                       |
| High | As with Low, but with aggravating factor C |

| $C$ | $B$ | $A$ | $T_{low}$ | $T_{high}$ |
|-----|-----|-----|-----------|------------|
| 0   | 0   | 0   | 0         | 0          |
| 0   | 0   | 1   | 1         | 0          |
| 0   | 1   | 0   | 1         | 0          |
| 0   | 1   | 1   | 1         | 0          |
| 1   | 0   | 0   | 0         | 0          |
| 1   | 0   | 1   | 0         | 1          |
| 1   | 1   | 0   | 0         | 1          |
| 1   | 1   | 1   | 0         | 1          |

Equations:
* $T_{low} = (A + B) \bar{C}$
* $T_{high} = (A + B) C$

## Example 8

Suppose there are now two aggavating factors:

| Band | Input                                          |
|------|------------------------------------------------|
| Low  | A, B                                           |
| High | As with Low, but with aggravating factors C, D |

| $D$ | $C$ | $B$ | $A$ | $T_{low}$ | $T_{high}$ |
|-----|-----|-----|-----|-----------|------------|
| 0   | 0   | 0   | 0   | 0         | 0          |
| 0   | 0   | 0   | 1   | 1         | 0          |
| 0   | 0   | 1   | 0   | 1         | 0          |
| 0   | 0   | 1   | 1   | 1         | 0          |
| 0   | 1   | 0   | 0   | 0         | 0          |
| 0   | 1   | 0   | 1   | 0         | 1          |
| 0   | 1   | 1   | 0   | 0         | 1          |
| 0   | 1   | 1   | 1   | 0         | 1          |
| 1   | 0   | 0   | 0   | 0         | 0          |
| 1   | 0   | 0   | 1   | 0         | 1          |
| 1   | 0   | 1   | 0   | 0         | 1          |
| 1   | 0   | 1   | 1   | 0         | 1          |
| 1   | 1   | 0   | 0   | 0         | 0          |
| 1   | 1   | 0   | 1   | 0         | 1          |
| 1   | 1   | 1   | 0   | 0         | 1          |
| 1   | 1   | 1   | 1   | 0         | 1          |

Equations:
* $T_{low} = (A + B) \overline{(C + D)} = (A + B) \bar{C} \bar{D}$
* $T_{high} = (A + B) (C + D)$

## Example 9

There are three bands and the High band is composed of two aggravating factors.

| Band   | Input                                             |
|--------|---------------------------------------------------|
| Low    | A, B                                              |
| Medium | C, D                                              |
| High   | As with Medium, but with aggravating factors E, F |


| $F$ | $E$ | $D$ | $C$ | $B$ | $A$ | $T_{low}$ | $T_{medium}$ | $T_{high}$ |
|-----|-----|-----|-----|-----|-----|-----------|--------------|------------|
| 0   | 0   | 0   | 0   | 0   | 0   | 0         | 0            | 0          |
| 0   | 0   | 0   | 0   | 0   | 1   | 1         | 0            | 0          |
| 0   | 0   | 0   | 0   | 1   | 0   | 1         | 0            | 0          |
| 0   | 0   | 0   | 0   | 1   | 1   | 1         | 0            | 0          |
| 0   | 0   | 0   | 1   | 0   | 0   | 0         | 1            | 0          |
| 0   | 0   | 0   | 1   | 0   | 1   | 0         | 1            | 0          |
| 0   | 0   | 0   | 1   | 1   | 0   | 0         | 1            | 0          |
| 0   | 0   | 0   | 1   | 1   | 1   | 0         | 1            | 0          |
| 0   | 0   | 1   | 0   | 0   | 0   | 0         | 1            | 0          |
| 0   | 0   | 1   | 0   | 0   | 1   | 0         | 1            | 0          |
| 0   | 0   | 1   | 0   | 1   | 0   | 0         | 1            | 0          |
| 0   | 0   | 1   | 0   | 1   | 1   | 0         | 1            | 0          |
| 0   | 0   | 1   | 1   | 0   | 0   | 0         | 1            | 0          |
| 0   | 0   | 1   | 1   | 0   | 1   | 0         | 1            | 0          |
| 0   | 0   | 1   | 1   | 1   | 0   | 0         | 1            | 0          |
| 0   | 0   | 1   | 1   | 1   | 1   | 0         | 1            | 0          |
| 0   | 1   | 0   | 0   | 0   | 0   | 0         | 0            | 0          |
| 0   | 1   | 0   | 0   | 0   | 1   | 0         | 0            | 0          |
| 0   | 1   | 0   | 0   | 1   | 0   | 0         | 0            | 0          |
| 0   | 1   | 0   | 0   | 1   | 1   | 0         | 0            | 0          |
| 0   | 1   | 0   | 1   | 0   | 0   | 0         | 0            | 1          |
| 0   | 1   | 0   | 1   | 0   | 1   | 0         | 0            | 1          |
| 0   | 1   | 0   | 1   | 1   | 0   | 0         | 0            | 1          |
| 0   | 1   | 0   | 1   | 1   | 1   | 0         | 0            | 1          |
| 0   | 1   | 1   | 0   | 0   | 0   | 0         | 0            | 1          |
| 0   | 1   | 1   | 0   | 0   | 1   | 0         | 0            | 1          |
| 0   | 1   | 1   | 0   | 1   | 0   | 0         | 0            | 1          |
| 0   | 1   | 1   | 0   | 1   | 1   | 0         | 0            | 1          |
| 0   | 1   | 1   | 1   | 0   | 0   | 0         | 0            | 1          |
| 0   | 1   | 1   | 1   | 0   | 1   | 0         | 0            | 1          |
| 0   | 1   | 1   | 1   | 1   | 0   | 0         | 0            | 1          |
| 0   | 1   | 1   | 1   | 1   | 1   | 0         | 0            | 1          |
| 1   | 0   | 0   | 0   | 0   | 0   | 0         | 0            | 0          |
| 1   | 0   | 0   | 0   | 0   | 1   | 0         | 0            | 0          |
| 1   | 0   | 0   | 0   | 1   | 0   | 0         | 0            | 0          |
| 1   | 0   | 0   | 0   | 1   | 1   | 0         | 0            | 0          |
| 1   | 0   | 0   | 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 0   | 0   | 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 0   | 0   | 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 0   | 0   | 1   | 1   | 1   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0   | 0   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0   | 0   | 1   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0   | 1   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 0   | 1   | 1   | 0         | 0            | 1          |
| 1   | 0   | 1   | 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 0   | 1   | 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 0   | 1   | 1   | 1   | 1   | 0         | 0            | 1          |
| 1   | 1   | 0   | 0   | 0   | 0   | 0         | 0            | 0          |
| 1   | 1   | 0   | 0   | 0   | 1   | 0         | 0            | 0          |
| 1   | 1   | 0   | 0   | 1   | 0   | 0         | 0            | 0          |
| 1   | 1   | 0   | 0   | 1   | 1   | 0         | 0            | 0          |
| 1   | 1   | 0   | 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 1   | 0   | 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 1   | 0   | 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 1   | 0   | 1   | 1   | 1   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0   | 0   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0   | 0   | 1   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0   | 1   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 0   | 1   | 1   | 0         | 0            | 1          |
| 1   | 1   | 1   | 1   | 0   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 1   | 0   | 1   | 0         | 0            | 1          |
| 1   | 1   | 1   | 1   | 1   | 0   | 0         | 0            | 1          |
| 1   | 1   | 1   | 1   | 1   | 1   | 0         | 0            | 1          |

Equations:
* $T_{low} = (A + B) \overline{(C + D)} \cdot \overline{(E + F)} = (A + B) \bar{C} \bar{D} \bar{E} \bar{F}$
* $T_{medium} = (C + D) \overline{(E + F)} = (C + D) \bar{E} \bar{F}$
* $T_{high} = (C + D)(E + F)$