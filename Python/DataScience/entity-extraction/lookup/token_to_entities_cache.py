from functools import lru_cache
from typing import List, Optional, Set, Tuple

from domain import Tokens, assert_token_valid, assert_tokens_valid


class TokenToEntitiesCache:
    """Token-to-entity IDs cache."""

    def __init__(self) -> None:
        self._cache = {}

    def add(self, token: str, entity_ids: Optional[Set[str]]) -> None:
        """Add a token and its entity IDs to the cache."""

        assert_token_valid(token)
        assert entity_ids is None or type(entity_ids) == set

        if entity_ids is None:
            self._cache[token] = {}
        else:
            self._cache[token] = entity_ids

    def retain(self, tokens: Tokens) -> None:
        """Retain the input tokens in the cache (removing others)."""

        assert_tokens_valid(tokens)

        required = set(tokens)
        to_remove = set()
        for token in self._cache.keys():
            if token not in required:
                to_remove.add(token)

        for token in to_remove:
            del self._cache[token]

    def required(self, tokens: Tokens) -> List[str]:
        """Returns the tokens and their entities that are required."""

        assert_tokens_valid(tokens)

        return [t for t in tokens if t not in self._cache.keys()]

    def entities_in_common(self, tokens: Tokens) -> Set[str]:
        """Returns a set of the entity IDs in common for all tokens."""

        assert_tokens_valid(tokens)
        return self._entities_in_common_lru(tuple(tokens))

    @lru_cache(maxsize=100)
    def _entities_in_common_lru(self, tokens: Tuple[str]) -> Set[str]:

        # Check that all tokens exist in the cache
        for t in tokens:
            if t not in self._cache.keys():
                raise Exception(f"cache miss for token: {t}")

        # If there's only one token then just return that token's entity IDs
        if len(tokens) == 1:
            return self._cache[tokens[0]]

        # Entities in common with the first two tokens
        result = self._cache[tokens[0]].intersection(self._cache[tokens[1]])

        # Find the entities in the common for the remaining tokens
        for idx in range(2, len(tokens)):
            result = result.intersection(self._cache[tokens[idx]])
            if len(result) == 0:
                return set()

        return result

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return f"TokenToEntitiesCache(tokens={list(self._cache.keys())})"
