from typing import List, Tuple
from loguru import logger
from domain import Tokens, assert_probability_valid, assert_token_valid
from entity.matcher import EntityMatcher, ProbabilisticMatch
from likelihood.likelihood_add_remove import LikelihoodAddRemoveFn
from lookup.lookup import Lookup

from positions_compiled_c import calc_positions
from adds_removes import adds_removes_from_positions


def subdivide_text(
    num_tokens: int, max_segment_length: int, max_window: int
) -> List[Tuple[int, int]]:
    """Sub-divide the text into segments for processing."""

    assert type(num_tokens) == int and num_tokens > 0
    assert type(max_segment_length) == int and max_segment_length >= max_window
    assert type(max_window) == int and max_window > 0

    # All of the tokens fit within a single segment
    if num_tokens <= max_segment_length:
        return [(0, num_tokens)]

    # First segment
    result = [(0, max_segment_length)]

    # Remaining segments
    while result[-1][1] < num_tokens:
        start = result[-1][1] - max_window + 1
        end = min(start + max_segment_length, num_tokens)
        result.append((start, end))

    return result


class EntityMatcherAddRemove(EntityMatcher):
    def __init__(
        self,
        lookup: Lookup,
        likelihood: LikelihoodAddRemoveFn,
        min_window: int,
        max_window: int,
        min_probability: float,
        max_entity_id: int,
    ):
        assert isinstance(lookup, Lookup)
        assert isinstance(likelihood, LikelihoodAddRemoveFn)
        assert type(min_window) == int and min_window > 0
        assert type(max_window) == int and max_window >= min_window
        assert_probability_valid(min_probability)
        assert type(max_entity_id) == int and max_entity_id > 0

        # Store the parameters
        self._lookup = lookup
        self._likelihood = likelihood
        self._min_window = min_window
        self._max_window = max_window
        self._min_probability = min_probability
        self._max_entity_id = max_entity_id

        # List of tokens passed to this class
        self._tokens: Tokens = []

        # Initialise the list of matches
        self._matches: List[ProbabilisticMatch] = []

        # Entity IDs that match each token
        self._entity_ids_str: List[str] = []

    def next_token(self, token: str) -> None:
        """Receive the next token in the text."""

        assert_token_valid(token)
        self._tokens.append(token)

        # Look up the entity IDs that match the token
        entity_ids_str = self._lookup.entity_ids_for_token_string(token)
        if entity_ids_str is None:
            self._entity_ids_str.append("")
        else:
            self._entity_ids_str.append(entity_ids_str)

    def get_matches(self) -> List[ProbabilisticMatch]:
        """Return entity extraction results."""

        # Determine the minimum count of an entity for it to be tested
        min_count = max(
            1, self._likelihood.min_count(self._min_window, self._min_probability)
        )
        logger.debug(
            f"Minimum number of times the entity must appear for evaluation: {min_count}"
        )

        # Divide the text into segments that can be processed by the compiled C
        # code. The code uses 8 bits to represent a position, so the maximum
        # segment is 256.
        start_ends = subdivide_text(len(self._entity_ids_str), 255, self._max_window)
        logger.debug(f"Processing text in {len(start_ends)} segment(s)")

        for start_idx, end_idx in start_ends:
            sub_entity_ids = self._entity_ids_str[start_idx:end_idx]

            # Call compiled C code to find the entity positions
            s = "|".join(sub_entity_ids)
            position_results = calc_positions(
                s.encode(), self._max_entity_id, min_count
            )

            # Check the positions were calculated successfully
            if len(position_results.error_message) > 0:
                raise Exception(position_results.error_message)

            logger.debug(
                f"Number of entities with positions to evaluate: {len(position_results.results)}"
            )

            # Walk through each of the entities and their matching token positions
            # for the entities that have been seen the required minimum number of
            # times
            for entity_result in position_results.results:
                entity_id = entity_result.entity_id
                positions = entity_result.pos

                # Get the number of tokens for the entity
                n_e = self._lookup.num_tokens_for_entity(entity_id)
                assert n_e is not None

                windows = adds_removes_from_positions(
                    positions, n_e, self._min_window, self._max_window
                )

                for start, end, n_adds, n_removes in windows:

                    # Calculate the likelihood of the tokens given the entity
                    prob = self._likelihood.calc(n_adds, n_removes, n_e)

                    # If the likelihood is above the threshold, then store the
                    # match if it hasn't been seen before
                    if prob > self._min_probability:
                        m = ProbabilisticMatch(
                            start=start + start_idx,  # Apply the segment offset
                            end=end + start_idx,
                            entity_id=entity_id,
                            probability=prob,
                        )
                        if m not in self._matches:
                            self._matches.append(m)

        return self._matches

    def reset(self) -> None:
        """Reset the matcher."""

        self._tokens = []
        self._matches = []
        self._entity_ids_str = []
