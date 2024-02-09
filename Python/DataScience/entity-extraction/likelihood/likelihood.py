from abc import ABC, abstractmethod
from functools import lru_cache
import math

from domain import Tokens, assert_probability_valid, assert_tokens_valid


class LikelihoodFunction(ABC):
    @abstractmethod
    def calc(self, actual_tokens: Tokens, entity_tokens: Tokens) -> float:
        """Calculate the likelihood of the actual_tokens given the entity tokens."""
        pass


class LikelihoodFunctionProbMissing(LikelihoodFunction):
    def __init__(self, p_m: float):
        assert_probability_valid(p_m)
        self._p_m = p_m

    def calc(self, actual_tokens: Tokens, entity_tokens: Tokens) -> float:
        """Calculate the likelihood of the actual_tokens given the entity tokens."""
        assert_tokens_valid(actual_tokens)
        assert_tokens_valid(entity_tokens)

        # Number of tokens present
        n_p = len(set(entity_tokens).intersection(set(actual_tokens)))

        # Number of tokens missing
        n_m = len(set(entity_tokens).difference(set(actual_tokens)))

        assert n_p + n_m == len(entity_tokens)

        p = ((1 - self._p_m) ** n_p) * (self._p_m**n_m)
        assert_probability_valid(p)

        return p


class LikelihoodFunctionLogistic(LikelihoodFunction):
    """Calculate the likelihood p(T|E) using a logistic function."""

    def __init__(self, k: float, x0: float):
        assert type(k) == float
        assert type(x0) == float

        self._k = k
        self._x0 = x0

    def calc(self, actual_tokens: Tokens, entity_tokens: Tokens) -> float:
        """Calculate the likelihood of the actual_tokens given the entity tokens."""
        assert_tokens_valid(actual_tokens)
        assert_tokens_valid(entity_tokens)

        # Number of tokens present
        n_p = len(set(entity_tokens).intersection(set(actual_tokens)))

        # Proportion of tokens present
        prop = n_p / len(entity_tokens)

        # Probability
        return self._calc_prob(prop)

    @lru_cache(maxsize=100)
    def _calc_prob(self, prop: float) -> float:
        """Calculate the probability of the proportion of tokens."""
        if prop == 1.0:
            return 1.0
        elif prop == 0.0:
            return 0.0

        y = 1 / (1 + math.exp(-self._k * (prop - self._x0)))
        assert_probability_valid(y)

        return y
