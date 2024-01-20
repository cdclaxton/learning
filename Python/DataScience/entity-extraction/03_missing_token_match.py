# This script implements a method to find matching entities in a corpus when
# the text may have missing tokens.
#
# The implementation assumes that the tokens in an entity are unique.
import math

from entity.sequence import correct_sequence
from lookup.lookup import Lookup


def find_entities(lookup, text_tokens, min_width, max_width, p_m, x0, k):
    """Find entities in the text."""

    assert type(lookup) == Lookup
    assert type(text_tokens) == list and len(text_tokens) > 0
    assert type(min_width) == int
    assert type(max_width) == int
    assert min_width <= max_width
    assert 0.0 <= p_m <= 1.0

    matches = []
    matches_logistic = []

    # Walk through each of the window widths
    for window_width in range(min_width, max_width + 1):
        for start_idx in range(0, len(text_tokens) - window_width):
            # Subset of the token to check
            end_index = start_idx + window_width
            assert end_index < len(text_tokens)
            text_tokens_subset = text_tokens[start_idx:end_index]

            # Find matching entries in the lookup given the text tokens
            entries = lookup.matching_entries(text_tokens_subset)
            if entries is None:
                continue

            for entry_idx in entries:
                entry_tokens = lookup.tokens_for_entry(entry_idx)
                if correct_sequence(entry_tokens, text_tokens_subset):
                    # Match using a simple likelihood function
                    matches.append(
                        ProbabilisticMatch(
                            start_idx,
                            end_index,
                            window_width,
                            entry_idx,
                            likelihood(entry_tokens, text_tokens_subset, p_m),
                        )
                    )

                    # Match using the logistic likelihood function
                    matches_logistic.append(
                        ProbabilisticMatch(
                            start_idx,
                            end_index,
                            window_width,
                            entry_idx,
                            likelihood_logistic(
                                entry_tokens, text_tokens_subset, k, x0
                            ),
                        )
                    )

    return matches, matches_logistic


if __name__ == "__main__":
    # Entries to split where a token is denoted by a single letter
    entries = ["AB", "ABD", "ABCD", "ABCDE"]

    # Create a lookup from a token to the entries to which it occurs and a
    # lookup from the entry to its tokens
    lookup = Lookup()

    for idx, entry in enumerate(entries):
        tokens = [t for t in entry]
        lookup.add(idx, tokens)

    # Index:        0    1    2    3    4    5    6    7    8
    text_tokens = ["A", "E", "A", "B", "F", "A", "C", "D", "F"]

    matches, matches_logistic = find_entities(
        lookup, text_tokens, min_width=2, max_width=5, p_m=0.1, x0=0.5, k=10.0
    )

    # Sort the matches by their posterior probability
    matches = sorted(matches, key=lambda m: m.probability, reverse=True)
    for m in matches:
        text = text_tokens[m.start : m.end]
        entity = lookup.tokens_for_entry(m.entry_index)
        print(f"Text: {text}, Entity: {entity} -> Prob: {m.probability}")

    matches_logistic = sorted(
        matches_logistic, key=lambda m: m.probability, reverse=True
    )
    for m in matches_logistic:
        text = text_tokens[m.start : m.end]
        entity = lookup.tokens_for_entry(m.entry_index)
        print(f"[Logistic] Text: {text}, Entity: {entity} -> Prob: {m.probability}")
