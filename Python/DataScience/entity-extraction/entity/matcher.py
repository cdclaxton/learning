from abc import ABC, abstractmethod
from typing import Any, Dict, List

from domain import Tokens
from evaluator.evaluator import EntitySpan, calc_error


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
    def next_token(self, token) -> None:
        """Receive the next token in the text."""
        pass

    @abstractmethod
    def get_matches(self) -> List[ProbabilisticMatch]:
        """Return entity extraction results."""
        pass

    def get_matches_above_threshold(self, threshold: float) -> List[EntitySpan]:
        """Get entity matches above a given threshold."""

        assert type(threshold) == float
        assert 0.0 <= threshold <= 1.0

        return [
            EntitySpan(match.start, match.end, match.entry_index)
            for match in self.get_matches()
            if match.probability >= threshold
        ]

    @abstractmethod
    def reset(self) -> None:
        """Reset the matcher."""
        pass


def feed_entity_matchers(
    text_tokens: Tokens, entity_matchers: Dict[Any, EntityMatcher]
) -> None:
    """Feed the tokens into each of the entity matchers."""

    assert isinstance(text_tokens, list), f"expected a list, got {type(text_tokens)}"
    assert isinstance(
        entity_matchers, dict
    ), f"expected a dict, got {type(entity_matchers)}"
    assert all([isinstance(em, EntityMatcher) for em in entity_matchers.values()])

    for token in text_tokens:
        for _, em in entity_matchers.items():
            em.next_token(token)


def threshold_matcher_results(
    entity_matchers: Dict[Any, EntityMatcher], threshold: float
) -> Dict[Any, List[EntitySpan]]:
    """Get the entities from each matcher for a given threshold."""

    assert type(entity_matchers) == dict
    assert all([isinstance(em, EntityMatcher) for em in entity_matchers.values()])
    assert type(threshold) == float
    assert 0.0 <= threshold <= 1.0

    return {
        key: matcher.get_matches_above_threshold(threshold)
        for key, matcher in entity_matchers.items()
    }


def calc_matcher_error(
    ground_truth: List[EntitySpan], matcher_results: Dict[Any, List[EntitySpan]]
) -> Dict[Any, int]:
    """Calculate the errors for each matcher."""

    return {
        key: calc_error(ground_truth, entity_spans)
        for key, entity_spans in matcher_results.items()
    }
