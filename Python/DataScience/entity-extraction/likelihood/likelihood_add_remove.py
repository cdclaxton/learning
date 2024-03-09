from functools import lru_cache, partial
from typing import Callable, Tuple
from domain import Tokens, assert_probability_valid, assert_tokens_valid
from likelihood.likelihood import LikelihoodFunction
from likelihood.piecewise_linear import piecewise_likelihood


def num_token_additions_removals(actual: Tokens, entity: Tokens) -> Tuple[int, int]:
    """Number of tokens that have been added and removed."""

    # Convert the lists to sets
    actual = set(actual)
    entity = set(entity)

    removed = entity.difference(actual)
    added = actual.difference(entity)

    return len(added), len(removed)


class LikelihoodFunctionAddRemove(LikelihoodFunction):
    """Likelihood function that uses the proportion of tokens added and removed."""

    def __init__(
        self,
        likelihood_add: Callable[[int], float],
        likelihood_remove: Callable[[int], float],
        n_max: int,
    ):
        self._likelihood_add = likelihood_add
        self._likelihood_remove = likelihood_remove
        self._n_max = n_max

        # Build the lookup table
        self._build_lookup()

    def _build_lookup(self) -> None:

        # The table is in the form of (n_tokens-1) x n_adds x n_removes
        self._lookup = [
            [
                [
                    self._calc_prob(n_tokens, n_additions, n_removals)
                    for n_removals in range(self._n_max + 1)
                ]
                for n_additions in range(self._n_max + 1)
            ]
            for n_tokens in range(1, self._n_max + 1)
        ]

    def calc(self, actual_tokens: Tokens, entity_tokens: Tokens) -> float:
        """Calculate the likelihood of the actual_tokens given the entity_tokens."""

        num_adds, num_removes = num_token_additions_removals(
            actual_tokens, entity_tokens
        )
        return self._calc_prob_using_lookup(len(entity_tokens), num_adds, num_removes)

    def _calc_prob_using_lookup(
        self, n_tokens: int, n_additions: int, n_removals: int
    ) -> float:
        return self._lookup[n_tokens - 1][n_additions][n_removals]

    def _calc_prob(self, n_tokens: int, n_additions: int, n_removals: int) -> float:
        return self._likelihood_add(n_additions / n_tokens) * self._likelihood_remove(
            n_removals / n_tokens
        )

    def min_count(self, min_window: int, min_prob: float) -> int:
        assert type(min_window) == int and min_window > 0
        assert_probability_valid(min_prob)

        min_count_to_prob = [
            (i, self._calc_prob(min_window, 0, min_window - i))
            for i in range(0, min_window + 1)
        ]

        for mc, prob in min_count_to_prob:
            if prob >= min_prob:
                return mc


def make_likelihood_symmetric(
    x0: float, p0: float, x1: float, p1: float, n_max: int
) -> LikelihoodFunctionAddRemove:
    """Make a LikelihoodFunctionAddRemove with a symmetric likelihood function."""

    assert type(n_max) == int and n_max > 0

    fn = partial(piecewise_likelihood, x0, p0, x1, p1)
    return LikelihoodFunctionAddRemove(fn, fn, n_max)


class LikelihoodAddRemoveFn:
    def __init__(
        self,
        likelihood_add: Callable[[int], float],
        likelihood_remove: Callable[[int], float],
    ):

        self._likelihood_add = likelihood_add
        self._likelihood_remove = likelihood_remove

    @lru_cache(maxsize=100)
    def calc(self, n_adds: int, n_removes: int, n_e: int) -> float:
        """Calculate the likelihood."""

        return self._likelihood_add(n_adds / n_e) * self._likelihood_remove(
            n_removes / n_e
        )

    def min_count(self, min_window: int, min_prob: float) -> int:
        assert type(min_window) == int and min_window > 0
        assert_probability_valid(min_prob)

        min_count_to_prob = [
            (i, self.calc(0, min_window - i, min_window))
            for i in range(0, min_window + 1)
        ]

        for mc, prob in min_count_to_prob:
            if prob >= min_prob:
                return mc


def make_likelihood_add_remove_symmetric(
    x0: float, p0: float, x1: float, p1: float
) -> LikelihoodFunctionAddRemove:
    """Make a LikelihoodAddRemoveFn with a symmetric likelihood function."""

    fn = partial(piecewise_likelihood, x0, p0, x1, p1)
    return LikelihoodAddRemoveFn(fn, fn)
