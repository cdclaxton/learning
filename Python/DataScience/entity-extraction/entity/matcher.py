from abc import ABC, abstractmethod
from typing import Any, Dict, List

from domain import *
from evaluator.evaluator import EntitySpan, calc_error


class ProbabilisticMatch:
    """Represents a probabilistic entity match in piece of text."""

    def __init__(self, start: int, end: int, entity_id: int, probability: float):
        assert_start_end_index_valid(start, end)
        assert_entity_id_valid(entity_id)
        assert_probability_valid(probability)

        self.start = start
        self.end = end
        self.entity_id = entity_id
        self.probability = probability

    def __repr__(self):
        return f"ProbabilisticMatch(start={self.start}, end={self.end}, entity_id={self.entity_id}, probability={self.probability})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if type(other) != ProbabilisticMatch:
            return False

        return (
            self.start == other.start
            and self.end == other.end
            and self.entity_id == other.entity_id
            and abs(self.probability - other.probability) < 1e-6
        )


class EntityMatcher(ABC):
    """Abstract entity matcher."""

    @abstractmethod
    def next_token(self, token: str) -> None:
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
            EntitySpan(match.start, match.end, match.entity_id)
            for match in self.get_matches()
            if match.probability >= threshold
        ]

    def get_sorted_matches_above_threshold(
        self, threshold: float
    ) -> List[ProbabilisticMatch]:
        """Get a sorted list of entity matches above a given threshold."""

        assert_probability_valid(threshold)

        matches = [m for m in self.get_matches() if m.probability > threshold]
        return sorted(matches, key=lambda m: m.probability, reverse=True)

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


def spans_overlap(start0: int, end0: int, start1: int, end1: int) -> bool:
    """Do the spans overlap?"""

    assert type(start0) == int and start0 >= 0
    assert type(end0) == int and end0 >= 0
    assert end0 >= start0
    assert type(start1) == int and start1 >= 0
    assert type(end1) == int and end1 >= 0
    assert end1 >= start1

    values0 = set(range(start0, end0 + 1))
    values1 = set(range(start1, end1 + 1))

    return len(values0.intersection(values1)) > 0


def most_likely_matches(
    matches: List[ProbabilisticMatch],
) -> List[List[ProbabilisticMatch]]:
    """Most likely matches for a given span."""

    assert type(matches) == list

    # Sort the matches in descending order of probability
    matches = sorted(matches, key=lambda m: m.probability, reverse=True)

    # Group assignment for each match
    group = 0
    assignment = [None for _ in matches]

    # Iterate through the matches until every one of them has been assigned to
    # a group
    while any([a is None for a in assignment]):

        # Find the first unassigned match from the sorted list of matches
        seed_idx = [idx for idx, a in enumerate(assignment) if a is None][0]

        # Assign the match to the new group
        assignment[seed_idx] = group

        for i in range(len(assignment)):

            # Skip over matches that have already been assigned to a group
            if assignment[i] is not None:
                continue

            # If the spans of the seed match and this match overlap, then add
            # this match to the same group as the seed match
            if spans_overlap(
                start0=matches[seed_idx].start,
                end0=matches[seed_idx].end,
                start1=matches[i].start,
                end1=matches[i].end,
            ):
                assignment[i] = group

        group += 1

    # Find the most likely matches for each group
    most_likely = []
    for grp in range(group):

        group_matches = [m for idx, m in enumerate(matches) if assignment[idx] == grp]
        assert len(group_matches) > 0

        # The group matches will already been in sort order
        max_prob_for_group = group_matches[0].probability
        assert_probability_valid(max_prob_for_group)

        # Retain matches with the same probability
        group_matches = [
            m for m in group_matches if m.probability == max_prob_for_group
        ]

        most_likely.append(group_matches)

    return most_likely
