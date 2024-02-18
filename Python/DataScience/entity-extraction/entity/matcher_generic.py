from typing import List
from domain import assert_probability_valid, assert_token_valid
from entity.matcher import EntityMatcher, ProbabilisticMatch
from entity.sequence import Window
from likelihood.likelihood import LikelihoodFunction
from lookup.lookup import Lookup
from loguru import logger


class GenericEntityMatcher(EntityMatcher):
    """Performs entity matching where the core logic is in the likelihood function."""

    def __init__(
        self,
        lookup: Lookup,
        likelihood: LikelihoodFunction,
        max_window_width: int,
        min_tokens: int,
        min_probability: float,
    ):
        assert isinstance(lookup, Lookup)
        assert isinstance(likelihood, LikelihoodFunction)
        assert type(max_window_width) == int
        assert max_window_width > 0
        assert type(min_tokens) == int and min_tokens > 0
        assert_probability_valid(min_probability)

        self._lookup = lookup
        self._likelihood = likelihood
        self._max_window_width = max_window_width
        self._min_tokens_to_check = min_tokens
        self._min_probability = min_probability

        self._window: Window = Window(max_window_width)
        self._matches: List[ProbabilisticMatch] = []

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

            calculated = set()
            for token in tokens_in_window:

                entity_ids = self._lookup.entity_ids_for_token(token)

                # Walk through each entity
                for entity_id in entity_ids:

                    if entity_id in calculated:
                        continue
                    calculated.add(entity_id)

                    # Get the tokens for the entity
                    entity_tokens = self._lookup.tokens_for_entity(entity_id)

                    # Calculate the likelihood of the tokens given the entity
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
        return self._matches

    def reset(self) -> None:
        """Reset the matcher."""
        self._window = Window(self._max_window_width)
        self._matches = []
