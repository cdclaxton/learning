from typing import List
from domain import assert_token_valid
from entity.matcher import EntityMatcher, ProbabilisticMatch
from entity.sequence import Window, correct_sequence
from likelihood.likelihood import LikelihoodFunction
from lookup.lookup import Lookup
from lookup.token_to_entities_cache import OptimisedTokenToEntitiesCache
from loguru import logger


class MissingTokenEntityMatcher(EntityMatcher):
    """Performs entity matching where tokens may be missing."""

    def __init__(
        self,
        lookup: Lookup,
        max_window_width: int,
        likelihood_function: LikelihoodFunction,
    ):
        assert isinstance(lookup, Lookup)
        assert type(max_window_width) == int
        assert max_window_width > 0
        assert isinstance(likelihood_function, LikelihoodFunction)

        self._lookup = lookup
        self._max_window_width = max_window_width
        self._window: Window = Window(max_window_width)
        self._likelihood_function: LikelihoodFunction = likelihood_function
        self._matches: List[ProbabilisticMatch] = []

        # Initialise a cache that optimises the calculation of entities in
        # common for a list of tokens
        self._token_to_entities_cache = OptimisedTokenToEntitiesCache(
            lookup.entity_ids_for_token
        )

    def next_token(self, token) -> None:
        """Receive the next token in the text."""

        assert_token_valid(token)

        # Adjust the window by adding the token
        self._window.add_token(token)

        # Get the tokens in the window and the absolute start and end indices of
        # the tokens in the text
        tokens_in_window, _, end_idx = self._window.get_tokens()
        logger.debug(f"Processing window: {tokens_in_window}")

        # If the aren't sufficient tokens in the window, then just return
        if len(tokens_in_window) < self._min_tokens_to_check:
            return

        # Walk from the last tokens to the first tokens
        for i in range(len(tokens_in_window) - self._min_tokens_to_check, -1, -1):
            tokens_to_check = tokens_in_window[i:]
            assert len(tokens_to_check) >= self._min_tokens_to_check

            # Get the entities in common for the tokens to check
            entity_ids, cache_used = self._token_to_entities_cache.get(tokens_to_check)

            # Walk through each of the entities in common
            for entity_id in entity_ids:

                # Get the tokens for the entity
                entity_tokens = self._lookup.tokens_for_entity(entity_id)

                # Check the tokens appear in the correct order
                if not correct_sequence(entity_tokens, tokens_to_check):
                    continue

                # Calculate the probability of a match
                prob = self._likelihood_function.calc(tokens_to_check, entity_tokens)

                if prob >= self._min_probability:
                    self._matches.append(
                        ProbabilisticMatch(
                            start=end_idx - len(tokens_to_check) + 1,
                            end=end_idx,
                            entity_id=entity_id,
                            probability=prob,
                        )
                    )

        logger.debug(
            f"Number of matches in this and previous windows: {len(self._matches)}"
        )

    def get_matches(self) -> List[ProbabilisticMatch]:
        """Return entity extraction results."""
        return self._matches

    def reset(self) -> None:
        """Reset the matcher."""
        self._window = Window(self._max_window_width)
        self._matches = []
