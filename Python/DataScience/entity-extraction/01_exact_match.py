# This script explores how to find exact matches in an efficient manner.

import random
from domain import EntityToTokens, TextGenerator, Tokens
from entity.matcher import (
    calc_matcher_error,
    feed_entity_matchers,
    threshold_matcher_results,
)
from entity.matcher_exact import ExactEntityMatcher, Tree, tree_from_entities
from evaluator.evaluator import EntitySpan
from typing import Tuple

from generator.generator import (
    generate_entities,
    make_generator_fns,
    make_uniform_num_entity_tokens_generator,
    random_entity_id,
)
from visualisation.visualisation import visualise_probabilistic_matches


def generate_ground_truth(
    min_text_tokens: int,
    max_text_tokens: int,
    text_generator: TextGenerator,
    entities: EntityToTokens,
) -> Tuple[Tokens, EntitySpan]:
    """Generate a ground-truth piece of text with a known entity."""

    assert type(min_text_tokens) == int and min_text_tokens > 0
    assert type(max_text_tokens) == int and max_text_tokens > 0

    # Number of tokens to the left and to right of the entity
    num_tokens_left = random.randint(min_text_tokens, max_text_tokens)
    num_tokens_right = random.randint(min_text_tokens, max_text_tokens)

    # Generate the text tokens
    tokens_left = text_generator(num_tokens_left)
    tokens_right = text_generator(num_tokens_right)

    # Select the entity
    entity_id = random_entity_id(entities)
    entity_tokens = entities[entity_id]

    # Ground truth entity span
    start = len(tokens_left)
    e = EntitySpan(start, start + len(entity_tokens) - 1, entity_id)

    # Create the text that includes the entity
    text = tokens_left[:]
    text.extend(entity_tokens)
    text.extend(tokens_right)

    return text, e


if __name__ == "__main__":
    n_tokens = 100
    prop_entity_tokens = 0.2
    min_num_entity_tokens = 6
    max_num_entity_tokens = 10
    min_text_tokens = 1
    max_text_tokens = 10

    n_entity_tokens_fn = make_uniform_num_entity_tokens_generator(
        min_num_entity_tokens, max_num_entity_tokens
    )
    num_entities = 20

    # Text and entity token generator
    text_generator, entity_generator = make_generator_fns(
        n_tokens, prop_entity_tokens, n_entity_tokens_fn
    )

    # Randomly generate entities
    entities = generate_entities(num_entities, entity_generator)

    # Create a tree data structure for holding the entities
    tree, max_window = tree_from_entities(entities)

    # Instantiate an exact entity matcher with a tree constructed from the
    # entities and an exact entity matcher with an empty tree
    exact_entity_matcher = ExactEntityMatcher(tree, max_window)
    exact_entity_matcher_empty_tree = ExactEntityMatcher(Tree(), max_window)

    # Create a random piece of text containing zero or more entities
    tokens, gt_entity_span = generate_ground_truth(
        min_text_tokens, max_text_tokens, text_generator, entities
    )

    # Run the exact entity matchers
    matchers = {
        "exact matcher": exact_entity_matcher,
        "exact matcher with an empty tree": exact_entity_matcher_empty_tree,
    }
    feed_entity_matchers(tokens, matchers)

    # Visualise the results
    print(
        visualise_probabilistic_matches(tokens, exact_entity_matcher._matches, entities)
    )

    # Get the entity matches
    entity_spans = threshold_matcher_results(matchers, 0.5)

    # Calculate the error
    errors = calc_matcher_error([gt_entity_span], entity_spans)
    print(f"Matcher errors: {errors}")
