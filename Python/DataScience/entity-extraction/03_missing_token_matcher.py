# This script implements a method to find matching entities in a corpus when
# the text may have missing tokens.
#
# The implementation assumes that the tokens in an entity are unique.

from entity.matcher import feed_entity_matchers
from entity.matcher_missing_token import MissingTokenEntityMatcher
from likelihood.likelihood import (
    LikelihoodFunctionLogistic,
    LikelihoodFunctionProbMissing,
)
from lookup.in_memory_lookup import InMemoryLookup
from visualisation.visualisation import (
    visualise_probabilistic_matches_over_threshold,
)


if __name__ == "__main__":
    # Entries to split where a token is denoted by a single letter
    entries = ["AB", "ABD", "ABCD", "ABCDE"]
    max_window = max([len(entry) for entry in entries])

    # Create a lookup from a token to the entries to which it occurs and a
    # lookup from the entry to its tokens
    lookup = InMemoryLookup()

    for idx, entry in enumerate(entries):
        tokens = [t for t in entry]
        lookup.add(f"e-{idx}", tokens)

    # Index:        0    1    2    3    4    5    6    7    8
    text_tokens = ["A", "E", "A", "B", "F", "A", "C", "D", "F"]

    # Entity matcher that has a constant probability of a token being missing
    likelihood1 = LikelihoodFunctionProbMissing(0.1)
    m1 = MissingTokenEntityMatcher(lookup, max_window, likelihood1)

    # Entity matcher that has a logistic function for the likelihood for the
    # proportion of the tokens being missing
    likelihood2 = LikelihoodFunctionLogistic(10.0, 0.5)
    m2 = MissingTokenEntityMatcher(lookup, max_window, likelihood2)

    # All entity matchers
    entity_matchers = {"constant prob missing": m1, "logistic likelihood function": m2}

    # Send the tokens to the entity matchers
    feed_entity_matchers(text_tokens, entity_matchers)

    # Visualise the results
    print("Constant probability of missing token matcher:")
    print(
        visualise_probabilistic_matches_over_threshold(
            text_tokens, m1._matches, lookup._entity_id_to_tokens, 0.001
        )
    )

    print("Logistic likelihood function missing token matcher:")
    print(
        visualise_probabilistic_matches_over_threshold(
            text_tokens, m2._matches, lookup._entity_id_to_tokens, 0.001
        )
    )
