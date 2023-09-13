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

## Exact extraction

If the tokens in the text are present exactly as provided in the corpus, i.e. in the same order and without any spelling mistakes, then the problem of finding matching tokens in the corpus is fairly trivial. In the example, the matching entry begins at index 2 and ends at index 4.

An efficient implementation of an algorithm to find exact matches using a tree data structure is provided in `exact_match.py`.

## Mutations to tokens

Tokens can be mutated in a number of ways:

* Additional character(s), e.g. 'Green' becomes 'Greens';
* Removal of character(s), e.g. 'Greens' becomes 'Green';
* Rearrangement of characters (i.e. changing their position but where the  characters in a token remain the same) typically introducing a spelling mistake, e.g. 'Green' becomes 'Grene';
* Mutation of a characters, e.g. 'Green' becomes 'Greed'.