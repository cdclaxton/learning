from abc import ABC, abstractmethod


class ProbabilisticMatch:
    """Represents a probabilistic entity match in piece of text."""

    def __init__(self, start, end, entry_index, probability):
        assert type(start) == int
        assert type(end) == int
        assert start <= end
        assert entry_index is not None
        assert type(probability) == float
        assert 0.0 <= probability <= 1.0

        self.start = start
        self.end = end
        self.entry_index = entry_index
        self.probability = probability

    def __repr__(self):
        return f"ProbabilisticMatch(start={self.start}, end={self.end}, entry_index={self.entry_index}, probability={self.probability})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if type(other) != ProbabilisticMatch:
            return False

        return (
            self.start == other.start
            and self.end == other.end
            and self.entry_index == other.entry_index
            and abs(self.probability - other.probability) < 1e-6
        )


class EntityMatcher(ABC):
    @abstractmethod
    def next_token(self, token):
        """Receive the next token in the text."""
        pass

    @abstractmethod
    def get_matches(self):
        """Return entity extraction results."""
        pass

    @abstractmethod
    def reset(self):
        """Reset the matcher."""
        pass


def find_entities(text_tokens, entity_matchers):
    assert isinstance(text_tokens, list), f"expected a list, got {type(text_tokens)}"
    assert isinstance(
        entity_matchers, dict
    ), f"expected a dict, got {type(entity_matchers)}"
    assert all([isinstance(em, EntityMatcher) for em in entity_matchers.values()])

    for token in range(text_tokens):
        for _, em in entity_matchers.items():
            em.next_token(em)
