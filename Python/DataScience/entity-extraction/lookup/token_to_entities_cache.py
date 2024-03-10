from functools import lru_cache
from typing import Callable, List, Optional, Set, Tuple

from domain import Tokens, assert_token_valid, assert_tokens_valid


def one_more(original: Set[str], new: Set[str]) -> Tuple[bool, Optional[str]]:
    """Does the new set have one more element than the origina set?"""

    assert type(original) == set
    assert type(new) == set

    # All elements in the new must be in the original
    if len(original.difference(new)) > 0:
        return False, None

    # Find elements in the new set that aren't in the original set
    extra = new.difference(original)
    if len(extra) == 1:
        return True, list(extra)[0]

    return False, None


class OptimisedTokenToEntitiesCache:

    def __init__(self, entity_getter: Callable[[str], Optional[Set[int]]]) -> None:
        self._entity_getter = entity_getter
        self._tokens = set()
        self._entities = set()

    def clear(self):
        """Clear the cache."""

        self._tokens: Set[str] = set()
        self._entities: Set[int] = set()

    def get(self, tokens: Tokens) -> Tuple[Set[int], bool]:
        """Get the entity IDs in common for the tokens."""

        assert_tokens_valid(tokens)

        # Set of new tokens for which entities in common are required
        new_tokens = set(tokens)

        # If there are no new tokens, just return the existing cached entities
        if new_tokens == self._tokens:
            return self._entities, True

        # Is there just one more token than in the cache?
        one_more_token, token = one_more(self._tokens, new_tokens)
        if one_more_token:
            cache_used = True
            extra_entities = self._entity_getter(token)
            if extra_entities is None:
                self._entities = set()
            else:
                self._entities = self._entities.intersection(extra_entities)

        else:
            cache_used = False
            for idx, token in enumerate(tokens):
                entities = self._entity_getter(token)
                if entities is None:
                    self._entities = set()
                    break
                elif idx == 0:
                    self._entities = entities
                else:
                    self._entities = self._entities.intersection(entities)

                if len(self._entities) == 0:
                    break

        self._tokens = new_tokens

        return self._entities, cache_used


class TokenToEntitiesCache:
    """Token-to-entity IDs cache."""

    def __init__(self) -> None:
        self._cache = {}

    def add(self, token: str, entity_ids: Optional[Set[int]]) -> None:
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

    def entities_in_common(self, tokens: Tokens) -> Set[int]:
        """Returns a set of the entity IDs in common for all tokens."""

        assert_tokens_valid(tokens)
        return self._entities_in_common_lru(tuple(tokens))

    @lru_cache(maxsize=100)
    def _entities_in_common_lru(self, tokens: Tuple[str]) -> Set[int]:

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
