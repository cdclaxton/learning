from abc import ABC, abstractmethod
from typing import Any, Dict, List

from domain import *
from evaluator.evaluator import EntitySpan, calc_error


class ProbabilisticMatch:
    """Represents a probabilistic entity match in piece of text."""

    def __init__(self, start, end, entity_id, probability):
        assert_start_end_index_valid(start, end)
        assert_entity_id_valid(entity_id)
        assert_probability_valid(probability)

        self._start = start
        self._end = end
        self._entity_id = entity_id
        self._probability = probability

    def __repr__(self):
        return f"ProbabilisticMatch(start={self._start}, end={self._end}, entity_id={self._entity_id}, probability={self._probability})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if type(other) != ProbabilisticMatch:
            return False

        return (
            self._start == other._start
            and self._end == other._end
            and self._entity_id == other._entity_id
            and abs(self._probability - other._probability) < 1e-6
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

        assert_probability_valid(threshold)

        return [
            EntitySpan(match._start, match._end, match._entity_id)
            for match in self.get_matches()
            if match._probability >= threshold
        ]

    def get_sorted_matches_above_threshold(
        self, threshold: float
    ) -> List[ProbabilisticMatch]:
        """Get a sorted list of entity matches above a given threshold."""

        assert_probability_valid(threshold)

        matches = [m for m in self._matches if m._probability > threshold]
        return sorted(matches, key=lambda m: m._probability, reverse=True)

    @abstractmethod
    def reset(self) -> None:
        """Reset the matcher."""
        pass


def feed_entity_matchers(
    text_tokens: Tokens, entity_matchers: Dict[Any, EntityMatcher]
) -> None:
    """Feed the tokens into each of the entity matchers."""

    assert_tokens_valid(text_tokens)
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
    assert_probability_valid(threshold)

    return {
        key: matcher.get_matches_above_threshold(threshold)
        for key, matcher in entity_matchers.items()
    }


def calc_matcher_error(
    ground_truth: List[EntitySpan], matcher_results: Dict[Any, List[EntitySpan]]
) -> Dict[Any, int]:
    """Calculate the errors for each matcher."""

    assert type(ground_truth) == list
    assert all([type(e) == EntitySpan for e in ground_truth])
    assert type(matcher_results) == dict

    return {
        key: calc_error(ground_truth, entity_spans)
        for key, entity_spans in matcher_results.items()
    }
