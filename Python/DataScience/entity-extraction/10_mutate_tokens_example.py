# This script demonstrates a method of mutating the tokens of
# an entity in order to generate test data for the extractor
# and resolver.
import random
import string
from nltk.tokenize import wordpunct_tokenize


def tokenise_text(text: str) -> list[str]:
    """Tokenise the text into tokens and make each token lowercase."""

    assert type(text) == str and len(text) > 0

    # Punctuation
    punct = set(string.punctuation)

    def only_punctuation(text: str) -> bool:
        """Is the text composed of just punctuation?"""
        return all([t in punct for t in text])

    # Tokenise the lowercase version of the text
    tokens = wordpunct_tokenize(text.lower())

    # Remove tokens that are only punctuation
    return [t for t in tokens if not only_punctuation(t)]


def mutate(tokens: list[str], min_tokens: int) -> list[str]:
    """Mutate tokens by adding and removing tokens."""

    assert type(tokens) == list
    assert all([type(t) == str for t in tokens])
    assert type(min_tokens) == int and min_tokens > 0

    # Make a copy of the tokens
    mutated_tokens = tokens[:]

    # Sample from a uniform distribution to determine the number of
    # tokens to remove
    max_tokens_to_remove = max(0, len(mutated_tokens) - min_tokens)
    n_tokens_to_remove = random.randint(0, max_tokens_to_remove)

    # Remove tokens at random
    for _ in range(n_tokens_to_remove):
        idx = random.randint(0, len(mutated_tokens) - 1)
        del mutated_tokens[idx]

    # Sample from a uniform distribution to determine the number of
    # tokens to add
    n_tokens_to_add = random.randint(0, 2)

    # Add tokens at random (this could be replaced with a token
    # from the Faker library for example)3457
    for i in range(n_tokens_to_add):
        idx = random.randint(1, len(mutated_tokens) - 1)
        mutated_tokens.insert(idx, f"--({i})--")

    return mutated_tokens


if __name__ == "__main__":

    # Define the entity to mutate (this would typically come as a
    # result of a database query to get an actual entity)
    example = "Flat 6, 10 Straight Street, Solihull, Birmingham, B12 4XY"
    print(f"Original entity: {example}")

    # Tokenise the string
    tokens = tokenise_text(example)

    # Mutate the entity and join the tokens to form a string
    mutated_tokens = mutate(tokens, 3)
    mutated = " ".join(mutated_tokens)
    print(f"Mutated entity: {mutated}")
