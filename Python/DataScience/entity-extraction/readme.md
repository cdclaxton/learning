# Token span extraction

This project explores ways to extract one or more contiguous tokens from a text where a large corpus of sets contiguous of tokens is available and where a token is defined as a sequence of alphanumeric characters with no whitespace or punctuation.

Suppose the corpus has an entry of "37 Straight Street". This entry can be tokenised into 3 elements:

```
["37", "Straight", "Street"].
```

A piece of text to undergo extraction is provided, such as "Go to 37 Straight Street at 1400". This would be tokenised to give:

```
["Go", "to", "37", "Straight", "Street", "at", "1400"].
```

The order of the scripts that were written and their descriptions is reflected in the structure of the sections below. The complexity of the solution was built up incrementally.

## Exact extraction

If the tokens in the text are present exactly as provided in the corpus, i.e. in the same order and without any spelling mistakes, then the problem of finding matching tokens in the corpus is fairly trivial. In the example, the matching entry begins at index 2 and ends at index 4.

A reasonably efficient implementation of an algorithm to find exact matches using a tree data structure is provided in `01_exact_match.py`. A more efficient approach would probably use a state machine.

## Extraction with missing tokens

Suppose tokens in the text are present in the same order as in the corpus, but that one or more tokens may be missing from the text. The probability that an entity may be in the text is uniform, i.e. no entity is anymore likely to appear than any other.

Bayes' theorem can be used to give the probability of the entity $E_i$ in the corpus matching a given text:

$$
p(E_i|T) = \frac{p(T|E_i) p(E_i)}{p(T)}.
$$

The prior probability of the entity is denoted $p(E_i)$ and the likelihood of the text given the entity is denoted $p(T|E_i)$. The normalisation term $p(T)$ is the probability of the text:

$$
p(T) = \sum_{i} p(T|E_i) p(E_i).
$$

If the prior probability $p(E_i)$ is constant for all $i$ then:

$$
\begin{align*}
p(E_i|T) &= \frac{p(T|E_i) p(E_i)}{p(T)} \\
 &= \frac{p(T|E_i) p(E_i)}{\sum_{i} p(T|E_i) p(E_i)} \\
 &= \frac{p(T|E_i)}{\sum_{i} p(T|E_i)}. \\
\end{align*}
$$

The likelihood function provides a measure of how likely a given entity is to have been written as the text. The probability that a token is missing is denoted $p_m$ and it assumed that the omissions are independent. The number of missing tokens in the text is denoted $n_m$ and the number present by $n_p$. Therefore, the likelihood function is given by:

$$
p(T|E_i) = 
\begin{cases} 
      (1-p_m)^{n_p} p_{m}^{n_{m}}  & \text{if text is a subset of entity $E_i$ and token order is correct} \\
      0 & \text{otherwise} \\
   \end{cases}
$$

Suppose the corpus consists of four entities:

```
E0: A B
E1: A B D
E2: A B C D
E3: A B C D E
```

and the text is:

```
T: A B D
```

The likelihoods of the text given the entities is:

$$
\begin{align*}
p(T | E_0) &= 0 \\
p(T | E_1) &= (1 - p_m)^3 \\
p(T | E_2) &= (1 - p_m)^3 p_m \\
p(T | E_3) &= (1 - p_m)^3 p_m^{2} \\
\end{align*}
$$

Therefore the posterior probabilities of the entities given the text are given by:

$$
\begin{align*}
p(E_0 | T) &= 0 \\
p(E_1 | T) &= \frac{(1 - p_m)^3}{ (1 - p_m)^3 + (1 - p_m)^3 p_m + (1 - p_m)^3 p_m^{2}} \\
p(E_2 | T) &= \frac{(1 - p_m)^3 p_m}{ (1 - p_m)^3 + (1 - p_m)^3 p_m + (1 - p_m)^3 p_m^{2} } \\
p(E_2 | T) &= \frac{(1 - p_m)^3 p_m^{2}}{ (1 - p_m)^3 + (1 - p_m)^3 p_m + (1 - p_m)^3 p_m^{2} } \\
\end{align*}
$$

The Python script `02_posterior_probs.py` computes the posterior probabilities for different values of $p_m$. If there is no chance a token is missing ($p_m = 0$) then:

$$
\begin{align*}
p(E_0 = [A,B] | T = [A,B,D]) &= 0 \\
p(E_1 = [A,B,D] | T = [A,B,D]) &= 1.0 \leftarrow \text{no missing tokens} \\
p(E_2 = [A,B,C,D] | T = [A,B,D]) &= 0.0 \leftarrow \text{1 missing token}\\
p(E_3 = [A,B,C,D,E] | T = [A,B,D]) &= 0.0 \leftarrow \text{2 missing tokens} \\
\end{align*}
$$

If instead there is a small chance of a missing token, i.e. $p_m$ = 0.1, then the posterior probabilities become:

$$
\begin{align*}
p(E_0 = [A,B] | T = [A,B,D]) &= 0 \\
p(E_1 = [A,B,D] | T = [A,B,D]) &= 0.901 \leftarrow \text{no missing tokens} \\
p(E_2 = [A,B,C,D] | T = [A,B,D]) &= 0.090 \leftarrow \text{1 missing token}\\
p(E_3 = [A,B,C,D,E] | T = [A,B,D]) &= 0.009 \leftarrow \text{2 missing tokens} \\
\end{align*}
$$

The script `03_missing_token_match.py` implements a method to find matching entities when tokens can be missing.

Using the script, it was identified that the likelihood function seems to be causing too large a drop off in the probability when just a single token was missing. Futhermore, the probability when all tokens are present decreases as the number of tokens increases, even though the entity is arguably much more specific.

In order to remedy this issue, the proportion of the tokens that are present was considered. This then requires a mapping from the proportion present to a probability. If all tokens are present, then a probability of 1 seems reasonable; equally, if all tokens are missing then the probability should be 0. There are in an infinite number of functions between the points $(0,0)$ amd $(1,1)$. The logistic function was chosen and is plotted in `04_logistic_function.py`.

The function is given by:

$$
y = \frac{1}{1 + \exp^{k(x - x_0)}}
$$

where $x_0$ is the $x$ position at which $y = 0.5$ and $k$ is steepness of the curve. The figure below shows the function for $k = 10$ and $x_0 = 0.5$.

![](./images/logistic_function.png)

## Mutations to tokens

Tokens can be mutated in a number of ways:

* Additional character(s), e.g. 'Green' becomes 'Greens';
* Removal of character(s), e.g. 'Greens' becomes 'Green';
* Rearrangement of characters (i.e. changing their position but where the  characters in a token remain the same) typically introducing a spelling mistake, e.g. 'Green' becomes 'Grene';
* Mutation of a characters, e.g. 'Green' becomes 'Greed'.

Bayes' theorem can be used to calculate the posterior likelihood of the $i^{th}$ entity given the text as before:

$$
p(E_i|T) = \frac{p(T|E_i) p(E_i)}{p(T)}
$$

but the likelihood function $p(T|E_i)$ needs to account for the potential mutations as opposed to just the proportion of tokens present.

There are variety of ways in which string distances can be calculated as shown in the table below.

| Algorithm name                            | Description                                                                               |
|-------------------------------------------|-------------------------------------------------------------------------------------------|
| Levenshtein distance                      | Allows deletion, insertion and substitution                                               |
| Damerau–Levenshtein distance              | Allows insertion, deletion, substitution and the transposition of two adjacent characters |
| Longest Common Subsequence (LCS) distance | Allows only insertion and deletion (i.e. not substitution)                                |
| Hamming distance                          | Allows only substitution (thus strings must be of the same length)                        |
| Jaro distance                             | Allows only transposition                                                                 |
