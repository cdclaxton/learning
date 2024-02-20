from collections import defaultdict
from typing import Generator, List, Tuple
from domain import (
    Tokens,
    assert_entity_id_valid,
    assert_probability_valid,
    assert_token_valid,
)
from entity.matcher import EntityMatcher, ProbabilisticMatch
from likelihood.likelihood import LikelihoodFunction
from lookup.lookup import Lookup
from loguru import logger


def calc_windows(
    num_tokens: int,
    min_window: int,
    max_window: int,
) -> Generator[Tuple[int, int], None, None]:
    """Calculate the windows positions."""

    assert type(num_tokens) == int and num_tokens > 0
    assert type(min_window) == int and min_window > 0
    assert type(max_window) == int and max_window >= min_window

    for start_idx in range(0, num_tokens - min_window + 1):
        for end_idx in range(start_idx + min_window - 1, num_tokens):
            if end_idx - start_idx + 1 > max_window:
                break

            yield (start_idx, end_idx)


class GenericEntityMatcher(EntityMatcher):
    """Performs entity matching where the core logic is in the likelihood function."""

    def __init__(
        self,
        lookup: Lookup,
        likelihood: LikelihoodFunction,
        min_window: int,
        max_window: int,
        min_probability: float,
    ):
        assert isinstance(lookup, Lookup)
        assert isinstance(likelihood, LikelihoodFunction)
        assert type(min_window) == int and min_window > 0
        assert type(max_window) == int and max_window >= min_window
        assert_probability_valid(min_probability)

        # Store the parameters
        self._lookup = lookup
        self._likelihood = likelihood
        self._min_window = min_window
        self._max_window = max_window
        self._min_probability = min_probability

        # List of tokens passed to this class
        self._tokens: Tokens = []

        # Entity IDs of entities that need to be checked as they match one or
        # more tokens in the text
        self._entity_id_to_count = defaultdict(int)

        # Initialise the list of matches
        self._matches: List[ProbabilisticMatch] = []

    def next_token(self, token) -> None:
        """Receive the next token in the text."""

        assert_token_valid(token)
        self._tokens.append(token)

        # Get a set of the entity IDs that contain the token
        entity_ids = self._lookup.entity_ids_for_token(token)
        if entity_ids is None:
            return

        for entity_id in entity_ids:
            self._entity_id_to_count[entity_id] += 1

    def _calc_matches_for_entity(
        self, start_idx: int, end_idx: int, entity_id: str
    ) -> None:
        """Calculate the matches in the text from start:end (inclusive) for a given entity."""

        assert type(start_idx) == int and start_idx >= 0
        assert type(end_idx) == int and start_idx <= end_idx < len(self._tokens)
        assert_entity_id_valid(entity_id)

        # Get the tokens for the entity
        entity_tokens = self._lookup.tokens_for_entity(entity_id)

        # Calculate the likelihood of the tokens given the entity
        tokens_to_check = self._tokens[start_idx : (end_idx + 1)]
        prob = self._likelihood.calc(tokens_to_check, entity_tokens)

        # If the likelihood is above the threshold, then store the match
        if prob > self._min_probability:
            self._matches.append(
                ProbabilisticMatch(
                    start=end_idx - len(tokens_to_check) + 1,
                    end=end_idx,
                    entity_id=entity_id,
                    probability=prob,
                )
            )

    def get_matches(self) -> List[ProbabilisticMatch]:
        """Return entity extraction results."""

        logger.debug(
            f"Number of entities matching tokens: {len(self._entity_id_to_count)}"
        )

        # Determine the minimum count of an entity for it to be tested
        min_count = self._likelihood.min_count(self._min_window, self._min_probability)
        logger.debug(
            f"Minimum number of times the entity must appear for evaluation: {min_count}"
        )

        # Walk through each entity first because getting the entity from the
        # lookup can be expensive
        num_tested = 0
        for entity_id, count in self._entity_id_to_count.items():

            # If the entity ID appears insufficiently, don't test it
            if count < min_count:
                continue

            num_tested += 1
            # Walk through each start and end position for the sub-window
            for start_idx, end_idx in calc_windows(
                num_tokens=len(self._tokens),
                min_window=self._min_window,
                max_window=self._max_window,
            ):

                # Calculate the matches for the entity in the sub-window
                self._calc_matches_for_entity(start_idx, end_idx, entity_id)

        logger.debug(f"Number of entities tested: {num_tested}")

        return self._matches

    def reset(self) -> None:
        """Reset the matcher."""

        self._tokens = []
        self._entity_ids = set()
        self._matches = []
