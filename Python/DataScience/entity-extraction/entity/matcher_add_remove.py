from typing import Generator, List, Set, Tuple
from loguru import logger
from domain import Tokens, assert_probability_valid, assert_token_valid
from entity.matcher import EntityMatcher, ProbabilisticMatch
from likelihood.likelihood_add_remove import LikelihoodAddRemoveFn
from lookup.lookup import Lookup
from metrics_compiled_c_arrays import calc_metrics
from positions_compiled_c import calc_positions


def adds_removes_from_positions(
    pos: List[int],
    n_entity_tokens: int,
    min_window: int,
    max_window: int,
) -> List[Tuple[int, int, int, int]]:

    assert type(pos) == list
    assert type(n_entity_tokens) == int and n_entity_tokens > 0
    assert type(min_window) == int and min_window > 0
    assert type(max_window) == int and max_window >= min_window

    result: List[Tuple[int, int, int, int]] = []
    if len(pos) == 1:
        return result

    for i in range(0, len(pos) - 1):
        for j in range(i + 1, len(pos)):

            # Number of text tokens
            n_t = pos[j] - pos[i] + 1

            if n_t < min_window:
                continue
            elif n_t > max_window:
                break

            # Number of tokens in common (in text and entity)
            n_c = j - i + 1

            # Number of tokens added
            n_adds = max(0, n_t - n_c)

            # Number of tokens remvoed
            n_removes = max(0, n_entity_tokens - n_c)

            result.append((pos[i], pos[j], n_adds, n_removes))

    return result


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
        self._current_token_index: int = -1

        # Initialise the list of matches
        self._matches: List[ProbabilisticMatch] = []

        # Entity IDs that match each token
        # self._entity_ids: List[Set[int]] = []
        self._entity_ids_str: List[str] = []

        # Entity ID to
        # - count is the number times the entity was seen
        # - start is the token index of the first match
        # - end is the token index of the last match
        # self._entity_id_to_count = Counter()
        # self._entity_id_to_start: dict[int, int] = dict()
        # self._entity_id_to_end: dict[int, int] = dict()

    def next_token(self, token: str) -> None:
        """Receive the next token in the text."""

        assert_token_valid(token)
        self._tokens.append(token)

        self._current_token_index += 1

        # Get a set of the entity IDs that contain the token
        # entity_ids = self._lookup.entity_ids_for_token(token)
        # print(f"Token: {token}, Entity IDs: {entity_ids}")
        # if entity_ids is None:
        #     self._entity_ids.append(set())
        #     self._entity_ids_str.append("")
        #     return

        # self._entity_ids.append(entity_ids)

        entity_ids_str = self._lookup.entity_ids_for_token_string(token)
        if entity_ids_str is None:
            self._entity_ids_str.append("")
        else:
            self._entity_ids_str.append(entity_ids_str)

        # Increment the count for the entities that match the token
        # for entity_id in self._entity_ids[-1]:
        #     self._entity_id_to_start.setdefault(entity_id, self._current_token_index)
        #     self._entity_id_to_end[entity_id] = self._current_token_index

        # self._entity_id_to_count.update(entity_ids)

    # def _calc_adds_removes(
    #     self, entity_id: int, start: int, end: int, n_e: int
    # ) -> Tuple[int, int]:

    #     # Number of tokens in common
    #     n_c = sum(
    #         [
    #             1 if entity_id in self._entity_ids[i] else 0
    #             for i in range(start, end + 1)
    #         ]
    #     )

    #     # Number of tokens in the text
    #     n_t = end - start + 1

    #     n_adds = n_t - n_c
    #     n_removes = n_e - n_c

    #     return n_adds, n_removes

    # def _calc_matches_for_entity(
    #     self, entity_id: int, start: int, end: int, n_e: int
    # ) -> None:

    #     # Find the number of tokens that have been added to and removed from
    #     # the entity
    #     n_adds, n_removes = self._calc_adds_removes(entity_id, start, end, n_e)

    #     # Calculate the likelihood of the tokens given the entity
    #     prob = self._likelihood.calc(n_adds, n_removes, n_e)

    #     # If the likelihood is above the threshold, then store the match
    #     if prob > self._min_probability:
    #         self._matches.append(
    #             ProbabilisticMatch(
    #                 start=start, end=end, entity_id=entity_id, probability=prob
    #             )
    #         )

    # def _calc_matches_for_entity_in_subwindows(self, entity_id: int) -> None:

    #     # Get the number of tokens for the entity
    #     n_e = self._lookup.num_tokens_for_entity(entity_id)
    #     assert n_e is not None

    #     # Walk through the sub-windows that emcompass the entity
    #     start_idx = self._entity_id_to_start[entity_id]
    #     end_idx = self._entity_id_to_end[entity_id]

    #     for start, end in calc_window_positions(
    #         start_idx, end_idx, self._min_window, self._max_window
    #     ):
    #         self._calc_matches_for_entity(entity_id, start, end, n_e)

    def get_matches(self) -> List[ProbabilisticMatch]:
        """Return entity extraction results."""

        # Determine the minimum count of an entity for it to be tested
        min_count = max(
            1, self._likelihood.min_count(self._min_window, self._min_probability)
        )
        logger.debug(
            f"Minimum number of times the entity must appear for evaluation: {min_count}"
        )

        # Call compiled C code to find the entity positions
        s = "|".join(self._entity_ids_str)
        position_results = calc_positions(s.encode(), self._max_entity_id, min_count)

        if len(position_results.error_message) > 0:
            raise Exception(position_results.error_message)

        logger.debug(
            f"Number of entities with positions to evaluate: {len(position_results.results)}"
        )

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

                # If the likelihood is above the threshold, then store the match
                if prob > self._min_probability:
                    self._matches.append(
                        ProbabilisticMatch(
                            start=start, end=end, entity_id=entity_id, probability=prob
                        )
                    )

        return self._matches

    # def get_matches(self) -> List[ProbabilisticMatch]:
    #     """Return entity extraction results."""

    #     # logger.debug(
    #     #     f"Number of entities matching tokens: {len(self._entity_id_to_count)}"
    #     # )

    #     # Determine the minimum count of an entity for it to be tested
    #     min_count = max(
    #         1, self._likelihood.min_count(self._min_window, self._min_probability)
    #     )
    #     logger.debug(
    #         f"Minimum number of times the entity must appear for evaluation: {min_count}"
    #     )

    #     # Call compiled C code
    #     s = "|".join(self._entity_ids_str)
    #     results = calc_metrics(s.encode(), self._max_entity_id, min_count)

    #     logger.debug(f"Number of entity IDs with sufficient counts: {len(results)}")

    #     for result in results:
    #         entity_id = result.entityId
    #         start_index = result.startIndex
    #         end_index = result.endIndex

    #         # Get the number of tokens for the entity
    #         n_e = self._lookup.num_tokens_for_entity(entity_id)
    #         assert n_e is not None

    #         for start, end in calc_window_positions(
    #             start_index, end_index, self._min_window, self._max_window
    #         ):
    #             self._calc_matches_for_entity(entity_id, start, end, n_e)

    #     # num_entities_count_over_threshold = 0
    #     # for entity_id in self._entity_id_to_count:

    #     #     # If the entity ID appears insufficiently, don't test it
    #     #     if self._entity_id_to_count[entity_id] < min_count:
    #     #         continue

    #     #     # Calculate the matches for the entity
    #     #     num_entities_count_over_threshold += 1
    #     #     self._calc_matches_for_entity_in_subwindows(entity_id)

    #     # logger.debug(f"Number of entities tested: {num_entities_count_over_threshold}")

    #     return self._matches

    def reset(self) -> None:
        """Reset the matcher."""

        self._tokens = []
        self._matches = []
        # self._entity_id_to_count = Counter()
        # self._entity_id_to_start = dict()
        # self._entity_id_to_end = dict()
