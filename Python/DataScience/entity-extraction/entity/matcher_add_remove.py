from typing import Generator, List, Set, Tuple

from loguru import logger
from domain import Tokens, assert_probability_valid, assert_token_valid
from entity.matcher import EntityMatcher, ProbabilisticMatch
from likelihood.likelihood_add_remove import LikelihoodAddRemoveFn
from lookup.lookup import Lookup


def calc_window_positions(
    start: int,
    end: int,
    min_window: int,
    max_window: int,
) -> Generator[Tuple[int, int], None, None]:
    """Calculate the windows positions."""

    assert type(start) == int and start >= 0, f"invalid start: {start}"
    assert type(end) == int and end >= start, f"invalid end: {end}"
    assert (
        type(min_window) == int and min_window > 0
    ), f"invalid min_window: {min_window}"
    assert (
        type(max_window) == int and max_window >= min_window
    ), f"invalid max window: {max_window}"

    for start_idx in range(start, end - min_window + 2):
        for end_idx in range(start_idx + min_window - 1, end + 1):
            if end_idx - start_idx + 1 > max_window:
                break

            yield (start_idx, end_idx)


class EntityMatcherAddRemove(EntityMatcher):
    def __init__(
        self,
        lookup: Lookup,
        likelihood: LikelihoodAddRemoveFn,
        min_window: int,
        max_window: int,
        min_probability: float,
    ):
        assert isinstance(lookup, Lookup)
        assert isinstance(likelihood, LikelihoodAddRemoveFn)
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
        self._current_token_index: int = -1

        # Initialise the list of matches
        self._matches: List[ProbabilisticMatch] = []

        # Entity IDs that match each token
        self._entity_ids: List[Set[str]] = []

        # Entity ID to
        # - count is the number times the entity was seen
        # - start is the token index of the first match
        # - end is the token index of the last match
        self._entity_id_to_count: dict[str, int] = dict()
        self._entity_id_to_start: dict[str, int] = dict()
        self._entity_id_to_end: dict[str, int] = dict()

    def next_token(self, token: str) -> None:
        """Receive the next token in the text."""

        assert_token_valid(token)
        self._tokens.append(token)

        self._current_token_index += 1

        # Get a set of the entity IDs that contain the token
        entity_ids = self._lookup.entity_ids_for_token(token)
        if entity_ids is None:
            self._entity_ids.append(set())
            return

        self._entity_ids.append(entity_ids)

        # Increment the count for the entities that match the token
        for entity_id in self._entity_ids[-1]:
            if entity_id not in self._entity_id_to_count:
                self._entity_id_to_count[entity_id] = 1
                self._entity_id_to_start[entity_id] = self._current_token_index
                self._entity_id_to_end[entity_id] = self._current_token_index

            else:
                self._entity_id_to_count[entity_id] += 1
                self._entity_id_to_end[entity_id] = self._current_token_index

    def _calc_adds_removes(
        self, entity_id: str, start: int, end: int, n_e: int
    ) -> Tuple[int, int]:

        # Number of tokens in common
        n_c = sum(
            [
                1 if entity_id in self._entity_ids[i] else 0
                for i in range(start, end + 1)
            ]
        )

        # Number of tokens in the text
        n_t = end - start + 1

        n_adds = n_t - n_c
        n_removes = n_e - n_c

        return n_adds, n_removes

    def _calc_matches_for_entity(
        self, entity_id: str, start: int, end: int, n_e: int
    ) -> None:

        logger.debug(f"Checking entity {entity_id} between {start} and {end}")

        # Find the number of tokens that have been added to and removed from
        # the entity
        n_adds, n_removes = self._calc_adds_removes(entity_id, start, end, n_e)

        # Calculate the likelihood of the tokens given the entity
        prob = self._likelihood.calc(n_adds, n_removes, n_e)

        # If the likelihood is above the threshold, then store the match
        if prob > self._min_probability:
            self._matches.append(
                ProbabilisticMatch(
                    start=start, end=end, entity_id=entity_id, probability=prob
                )
            )

    def _calc_matches_for_entity_in_subwindows(self, entity_id: str) -> None:

        # Get the number of tokens for the entity
        n_e = self._lookup.num_tokens_for_entity(entity_id)
        assert n_e is not None

        # Walk through the sub-windows that emcompass the entity
        start_idx = self._entity_id_to_start[entity_id]
        end_idx = self._entity_id_to_end[entity_id]

        for start, end in calc_window_positions(
            start_idx, end_idx, self._min_window, self._max_window
        ):
            self._calc_matches_for_entity(entity_id, start, end, n_e)

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

        num_entities_count_over_threshold = 0
        for entity_id in self._entity_id_to_count:

            # If the entity ID appears insufficiently, don't test it
            if self._entity_id_to_count[entity_id] < min_count:
                continue

            # Calculate the matches for the entity
            num_entities_count_over_threshold += 1
            self._calc_matches_for_entity_in_subwindows(entity_id)

        logger.debug(f"Number of entities tested: {num_entities_count_over_threshold}")

        return self._matches

    def reset(self) -> None:
        """Reset the matcher."""

        self._tokens: Tokens = []
        self._entity_id_to_count: dict[str, int] = dict()
        self._matches: List[ProbabilisticMatch] = []
        self._entity_id_to_count: dict[str, int] = dict()
        self._entity_id_to_start: dict[str, int] = dict()
        self._entity_id_to_end: dict[str, int] = dict()