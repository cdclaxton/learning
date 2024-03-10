import random
from typing import List

# Sequence of lower-case letters from a to z
letters: List[str] = [chr(x) for x in range(97, 123)]


def add_character(token: List[str]) -> None:
    """Add a character to the token. Mutates the list passed in."""

    assert type(token) == list
    assert len(token) > 0

    idx = random.randint(0, len(token) + 1)
    ch = random.choice(letters)
    token.insert(idx, ch)


def remove_character(token: List[str]) -> None:
    """Remove a character from the token. Mutates the list passed in."""

    assert type(token) == list
    assert len(token) > 0

    idx = random.randint(0, len(token) - 1)
    token.pop(idx)


def transpose_characters(token: List[str]) -> None:
    """Transpose (switch) two adjacent characters in the token."""

    assert type(token) == list
    assert len(token) > 1

    start = token[:]

    while token == start:
        # Choose a random start index
        indices = range(0, len(token) - 1)
        idx = random.choice(indices)

        # Switch the characters at (idx, idx+1)
        token[idx], token[idx + 1] = token[idx + 1], token[idx]


def substitute_character(token: List[str]) -> None:
    """Substitute a single character in the token."""

    assert type(token) == list
    assert len(token) > 0

    indices = list(range(0, len(token)))
    idx = random.choice(indices)

    before = token[idx]
    while before == token[idx]:
        token[idx] = random.choice(letters)


def random_mutation(token: List[str]) -> None:
    """Randomly mutate a token represented as a list of characters."""

    assert type(token) == list
    assert len(token) > 0

    fns = [add_character, substitute_character]
    if len(token) >= 2:
        fns.extend([transpose_characters, remove_character])

    fn = random.choice(fns)
    fn(token)


def random_mutation_str(token: List[str]) -> str:
    """Randomly mutate a token represented as a string."""

    assert type(token) == str

    ts = [t for t in token]
    return random_mutation(ts)


def random_mutations(token: List[str], num_mutations: int) -> str:
    """Perform num_mutations random mutations on a token."""

    assert type(token) == str
    assert num_mutations > 0

    ts = [t for t in token]

    for i in range(num_mutations):
        random_mutation(ts)

    return "".join(ts)
