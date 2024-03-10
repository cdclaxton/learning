import random
from typing import List, Callable, Tuple, Set, Dict
from functools import partial
from domain import EntityGenerator, EntityToTokens, Tokens, TextGenerator


def generate_tokens(n_tokens: int, max_index: int) -> Tokens:
    """Generate n_tokens tokens with replacement."""

    assert type(n_tokens) == int
    assert n_tokens > 0, f"n_tokens = {n_tokens}"
    assert type(max_index) == int
    assert max_index > 0, f"max_index = {max_index}"

    return [f"t{random.randint(0, max_index-1)}" for _ in range(n_tokens)]


def generate_entity_tokens(n_tokens: int, max_index: int) -> Tokens:
    """Generate n_tokens entity tokens without replacement."""

    assert type(n_tokens) == int and n_tokens > 0
    assert type(max_index) == int and max_index > 0
    assert n_tokens < max_index

    # Generate n_tokens unique tokens
    tokens: Set[str] = set()
    while len(tokens) < n_tokens:
        tokens.add(f"t{random.randint(0, max_index-1)}")

    # Convert the tokens to a list and then shuffle them
    entity: List[str] = list(tokens)
    random.shuffle(entity)
    return entity


def make_uniform_num_entity_tokens_generator(
    min_num: int, max_num: int
) -> Callable[[], int]:
    """Generate the number of entity tokens from a uniform distribution."""

    assert type(min_num) == int and min_num > 0
    assert type(max_num) == int and max_num >= min_num

    def f():
        return random.randint(min_num, max_num)

    return f


def make_generator_fns(
    n_tokens: int, prop_entity_tokens: float, n_entity_tokens_fn: Callable[[], int]
) -> Tuple[TextGenerator, EntityGenerator]:
    """Make a text generator and entity generator functions."""

    assert type(n_tokens) == int and n_tokens > 0
    assert type(prop_entity_tokens) == float and 0.0 <= prop_entity_tokens <= 1.0

    # Function to generate N random tokens for the text
    text_generator = partial(generate_tokens, max_index=n_tokens)

    # Number of entity tokens that could be used
    max_entity_tokens = int(n_tokens * prop_entity_tokens)

    # Function to generate entities
    def entity_generator() -> List[str]:
        num_entity_tokens = n_entity_tokens_fn()
        assert type(num_entity_tokens) == int
        assert num_entity_tokens > 0

        return generate_tokens(num_entity_tokens, max_entity_tokens)

    return text_generator, entity_generator


def generate_entities(
    num_entities: int, entity_token_generator: EntityGenerator
) -> EntityToTokens:
    """Generate num_entities entities using the entity token generator."""

    # Dict of entity ID to entity tokens
    entities = {}

    # Set of concatenated entity tokens
    concatenated_tokens = set()

    # Entity index
    entity_idx = 0

    while len(entities) < num_entities:
        # Generate a candidate list of tokens for the entity
        entity_tokens: Tokens = entity_token_generator()

        # Check that the entity tokens are unique
        concatenated = "".join(entity_tokens)
        if concatenated in concatenated_tokens:
            continue

        # Add the entity
        entities[entity_idx] = entity_tokens
        concatenated_tokens.add(concatenated)
        entity_idx += 1

    return entities


def random_entity_id(entities: EntityToTokens) -> str:
    """Randomly select an entity and return its entity ID."""

    return random.choice(list(entities.keys()))
