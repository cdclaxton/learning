from typing import List
from domain import assert_token_valid
from entity.matcher import EntityMatcher, ProbabilisticMatch
from entity.sequence import Window, correct_sequence
from likelihood.likelihood import LikelihoodFunction
from lookup.lookup import Lookup


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

    def next_token(self, token) -> None:
        """Receive the next token in the text."""

        assert_token_valid(token)

        # Adjust the window by adding the token
        self._window.add_token(token)

        # Get the tokens in the window and the absolute start and end indices of
        # the tokens in the text
        tokens_in_window, _, end_idx = self._window.get_tokens()

        for i in range(len(tokens_in_window)):
            tokens_to_check = tokens_in_window[i:]

            # Find matching entries in the lookup given the text tokens
            entries = self._lookup.matching_entries(tokens_to_check)
            if entries is None:
                continue

            for entry_idx in entries:
                entity_tokens = self._lookup.tokens_for_entity(entry_idx)
                if correct_sequence(entity_tokens, tokens_to_check):
                    m = ProbabilisticMatch(
                        start=end_idx - len(tokens_to_check) + 1,
                        end=end_idx,
                        entity_id=entry_idx,
                        probability=self._likelihood_function.calc(
                            tokens_to_check, entity_tokens
                        ),
                    )

                    self._matches.append(m)

    def get_matches(self) -> List[ProbabilisticMatch]:
        """Return entity extraction results."""
        return self._matches

    def reset(self) -> None:
        """Reset the matcher."""
        self._window = Window(self._max_window_width)
        self._matches = []
