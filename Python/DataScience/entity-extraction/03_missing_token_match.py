# This script implements a method to find matching entities in a corpus when
# the text may have missing tokens.
#
# The implementation assumes that the tokens in an entity are unique.
import math


class Lookup:
    """Holds two lookups."""

    def __init__(self):
        self.token_to_entries = {}
        self.entry_to_tokens = {}

    def add(self, entry_id, tokens):
        """Add an entry to the lookup."""
        assert type(entry_id) == int
        assert type(tokens) == list
        assert len(tokens) > 0

        assert entry_id not in self.entry_to_tokens, f"entry {entry_id} already exists"
        self.entry_to_tokens[entry_id] = tokens

        for t in tokens:
            if t not in self.token_to_entries:
                self.token_to_entries[t] = set()

            self.token_to_entries[t].add(entry_id)

    def tokens_for_entry(self, entry_id):
        """Get tokens for an entry given its ID."""

        assert type(entry_id) == int
        return self.entry_to_tokens.get(entry_id, None)

    def entries_for_token(self, token):
        return self.token_to_entries.get(token, None)


def test_lookup():
    """Unit tests for the Lookup class."""

    l = Lookup()

    # Add an entry
    l.add(0, ["80", "Straight", "Street"])

    assert l.tokens_for_entry(0) == ["80", "Straight", "Street"]
    assert l.tokens_for_entry(1) is None

    assert l.entries_for_token("80") == {0}
    assert l.entries_for_token("Straight") == {0}
    assert l.entries_for_token("Street") == {0}
    assert l.entries_for_token("Road") is None

    # Add a second entry
    l.add(1, ["80", "Broad", "Walk"])
    assert l.tokens_for_entry(0) == ["80", "Straight", "Street"]
    assert l.tokens_for_entry(1) == ["80", "Broad", "Walk"]

    assert l.entries_for_token("80") == {0, 1}
    assert l.entries_for_token("Broad") == {1}


def matching_entries(lookup, tokens):
    """Find the matching entries in the lookup given the tokens."""

    assert type(lookup) == Lookup
    assert type(tokens) == list
    assert len(tokens) > 0

    # Get the entries for each token
    for idx, t in enumerate(tokens):
        es = lookup.entries_for_token(t)

        if es is None:
            return None

        if idx == 0:
            entries = es
        else:
            entries = entries.intersection(es)

        # No entries match, so there's no point looking at any further tokens
        if entries is None or len(entries) == 0:
            return None

    return entries


def test_matching_entries():
    """Unit tests for matching_entries()."""

    l = Lookup()
    l.add(0, ["80", "Straight", "Street"])
    l.add(1, ["80", "River", "Street"])
    l.add(2, ["80", "Broad", "Walk"])

    # No matching tokens
    assert matching_entries(l, ["Street", "45"]) is None

    # Match one token
    assert matching_entries(l, ["80"]) == {0, 1, 2}
    assert matching_entries(l, ["Straight"]) == {0}
    assert matching_entries(l, ["Street"]) == {0, 1}
    assert matching_entries(l, ["Broad"]) == {2}
    assert matching_entries(l, ["Walk"]) == {2}

    # Match two tokens
    assert matching_entries(l, ["80", "Street"]) == {0, 1}
    assert matching_entries(l, ["80", "River"]) == {1}

    # Match three tokens
    assert matching_entries(l, ["80", "Street", "Straight"]) == {0}
    assert matching_entries(l, ["81", "Street", "Straight"]) is None


def correct_sequence(entity_tokens, text_tokens):
    """Are the tokens in the text in the correct order for the entity?"""

    assert type(entity_tokens) == list
    assert len(entity_tokens) > 0
    assert type(text_tokens) == list
    assert len(text_tokens) > 0

    if len(text_tokens) > len(entity_tokens):
        return False

    text_token_index = 0
    for entity_token in entity_tokens:
        if entity_token == text_tokens[text_token_index]:
            text_token_index += 1
            if text_token_index == len(text_tokens):
                break

    return text_token_index == len(text_tokens)


def test_correct_sequence():
    """Unit tests for correct_sequence()."""

    # Too many tokens in text for the likelihood function
    assert not correct_sequence(["A"], ["A", "B"])
    assert not correct_sequence(["A", "B"], ["A", "B", "C"])

    # Correct number of tokens, none missing
    assert correct_sequence(["A"], ["A"])
    assert correct_sequence(["A", "B"], ["A", "B"])
    assert correct_sequence(["A", "B", "C"], ["A", "B", "C"])

    # One missing token
    assert correct_sequence(["A", "B"], ["A"])
    assert correct_sequence(["A", "B"], ["B"])
    assert correct_sequence(["A", "B", "C"], ["A", "B"])
    assert correct_sequence(["A", "B", "C"], ["A", "C"])
    assert correct_sequence(["A", "B", "C"], ["B", "C"])

    # One missing token, incorrect order
    assert not correct_sequence(["A", "B", "C"], ["C", "B"])
    assert not correct_sequence(["A", "B", "C"], ["C", "A"])

    # One missing tokens and one extra token
    assert not correct_sequence(["A", "B"], ["A", "C"])

    # Two missing tokens
    assert correct_sequence(["A", "B", "C"], ["A"])
    assert correct_sequence(["A", "B", "C"], ["B"])
    assert correct_sequence(["A", "B", "C"], ["C"])
    assert correct_sequence(["A", "B", "C", "D"], ["A", "B"])
    assert correct_sequence(["A", "B", "C", "D"], ["A", "C"])
    assert correct_sequence(["A", "B", "C", "D"], ["A", "D"])
    assert correct_sequence(["A", "B", "C", "D"], ["B", "C"])
    assert correct_sequence(["A", "B", "C", "D"], ["B", "D"])
    assert correct_sequence(["A", "B", "C", "D"], ["C", "D"])

    # Two missing, incorrect order
    assert not correct_sequence(["A", "B", "C", "D"], ["C", "B"])

    # Two missing tokens and one extra token
    assert not correct_sequence(["A", "B", "C"], ["A", "D"])


def likelihood(entity_tokens, text_tokens, p_m):
    """Calculate the likelihood p(T|E)."""

    assert type(entity_tokens) == list
    assert len(entity_tokens) > 0
    assert type(text_tokens) == list
    assert len(text_tokens) > 0
    assert 0.0 <= p_m <= 1.0

    # Number of tokens present
    n_p = len(set(entity_tokens).intersection(set(text_tokens)))

    # Number of tokens missing
    n_m = len(set(entity_tokens).difference(set(text_tokens)))

    assert n_p + n_m == len(entity_tokens)

    p = ((1 - p_m) ** n_p) * (p_m**n_m)
    assert 0.0 <= p <= 1.0

    return p


def test_likelihood():
    """Unit tests for likelihood()."""

    def is_close(x, y):
        return abs(x - y) < 1e-6

    p_m = 0.2

    # None missing
    assert is_close(likelihood(["A"], ["A"], p_m), (1 - p_m))
    assert is_close(likelihood(["A", "B"], ["A", "B"], p_m), (1 - p_m) ** 2)

    # One missing
    assert is_close(likelihood(["A", "B"], ["A"], p_m), (1 - p_m) * p_m)
    assert is_close(likelihood(["A", "B", "C"], ["A", "C"], p_m), (1 - p_m) ** 2 * p_m)

    # Two missing
    assert is_close(likelihood(["A", "B", "C"], ["A"], p_m), (1 - p_m) * p_m**2)


def likelihood_logistic(entity_tokens, text_tokens, k, x0):
    """Calculate the likelihood p(T|E) using a logistic function."""

    assert type(entity_tokens) == list
    assert len(entity_tokens) > 0
    assert type(text_tokens) == list
    assert len(text_tokens) > 0
    assert type(k) == float
    assert type(x0) == float

    # Number of tokens present
    n_p = len(set(entity_tokens).intersection(set(text_tokens)))

    # Proportion of tokens present
    prop = n_p / len(entity_tokens)

    # Probability
    y = 1 / (1 + math.exp(-k * (prop - x0)))
    assert 0 <= y <= 1

    return y


class ProbabilisticMatch:
    def __init__(self, start, end, window_width, entry_index, probability):
        assert start <= end
        assert window_width > 0
        assert type(entry_index) == int
        assert 0.0 <= probability <= 1.0

        self.start = start
        self.end = end
        self.window_width = window_width
        self.entry_index = entry_index
        self.probability = probability

    def __repr__(self):
        return f"ProbabilisticMatch(start={self.start}, end={self.end}, window_width={self.window_width}, entry_index={self.entry_index}, probability={self.probability})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if type(other) != ProbabilisticMatch:
            return False

        return (
            self.start == other.start
            and self.end == other.end
            and self.window_width == other.window_width
            and self.entry_index == other.entry_index
            and self.probability == other.probability
        )


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
            text_tokens_subset = text_tokens[start_idx:(end_index)]

            # Find matching entries in the lookup given the text tokens
            entries = matching_entries(lookup, text_tokens_subset)
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
    # Run unit tests
    test_lookup()
    test_matching_entries()
    test_correct_sequence()
    test_likelihood()

    # Entries to split where a token is denoted by a single letter
    entries = ["AB", "ABD", "ABCD", "ABCDE"]

    # Create a lookup from a token the entries to which it occurs and a lookup
    # from the entry to its tokens
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
