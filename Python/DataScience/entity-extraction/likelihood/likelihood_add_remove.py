from functools import lru_cache, partial
from typing import Callable, Tuple
from domain import Tokens, assert_tokens_valid
from likelihood.likelihood import LikelihoodFunction
from likelihood.piecewise_linear import piecewise_likelihood


def num_token_additions_removals(actual: Tokens, entity: Tokens) -> Tuple[int, int]:
    """Number of tokens that have been added and removed."""

    assert_tokens_valid(actual)
    assert_tokens_valid(entity)

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
    ):
        self._likelihood_add = likelihood_add
        self._likelihood_remove = likelihood_remove

    def calc(self, actual_tokens: Tokens, entity_tokens: Tokens) -> float:
        """Calculate the likelihood of the actual_tokens given the entity_tokens."""

        num_adds, num_removes = num_token_additions_removals(
            actual_tokens, entity_tokens
        )

        return self._calc_prob(len(entity_tokens), num_adds, num_removes)

    @lru_cache(maxsize=100)
    def _calc_prob(self, n_tokens: int, n_additions: int, n_removals: int) -> float:
        return self._likelihood_add(n_additions / n_tokens) * self._likelihood_remove(
            n_removals / n_tokens
        )


def make_likelihood_symmetric(
    x0: float, p0: float, x1: float, p1: float
) -> LikelihoodFunctionAddRemove:
    """Make a LikelihoodFunctionAddRemove with a symmetric likelihood function."""

    fn = partial(piecewise_likelihood, x0, p0, x1, p1)
    return LikelihoodFunctionAddRemove(fn, fn)
