from typing import Callable, Dict, List


# List of tokens
Tokens = List[str]


def assert_token_valid(token: str) -> bool:
    """Checks that the token is valid."""
    assert type(token) == str, f"expected a str, got {type(token)}"
    assert len(token) > 0


def assert_tokens_valid(tokens: Tokens) -> None:
    """Checks that the tokens are valid."""
    assert type(tokens) == list, f"expected a list, got {type(list)}"
    for t in tokens:
        assert_token_valid(t)


# Function to generator N text tokens
TextGenerator = Callable[[int], Tokens]

# Function to generate an entity
EntityGenerator = Callable[[], Tokens]

# Dict of entity ID to tokens for the entity
EntityToTokens = Dict[int, Tokens]


def assert_entity_id_valid(entity_id: int) -> None:
    """Checks that the entity ID is valid."""
    assert type(entity_id) == int, f"expected an int, got {type(entity_id)}"
    assert entity_id >= 0, f"got entity ID: {entity_id}"


def assert_entity_to_tokens_valid(entity_to_tokens: EntityToTokens) -> None:
    """Checks that the entity to token mapping is valid."""
    assert (
        type(entity_to_tokens) == dict
    ), f"expected a dict, got {type(entity_to_tokens)}"

    # Check the entity IDs
    for e in entity_to_tokens.keys():
        assert_entity_id_valid(e)

    # Check the tokens
    for tokens in entity_to_tokens.values():
        assert_tokens_valid(tokens)


def assert_probability_valid(probability: float) -> None:
    """Checks that the probability is valid."""
    assert type(probability) == float, f"expected a float, got {type(probability)}"
    assert 0.0 <= probability <= 1.0, f"invalid probability: {probability}"


def assert_start_end_index_valid(start: int, end: int) -> None:
    """Check that the start and end indices are valid."""

    assert type(start) == int, f"expected an int, got {type(start)}"
    assert type(end) == int, f"expected an int, got {type(end)}"
    assert start >= 0, f"invalid start index: {start}"
    assert start <= end, f"invalid end index, start: {start}, end: {end}"
