from typing import Dict, List, Optional, Set

from domain import (
    Tokens,
    assert_entity_id_valid,
    assert_token_valid,
    assert_tokens_valid,
)
from lookup.lookup import Lookup


class InMemoryLookup(Lookup):
    """Holds two lookups in memory."""

    def __init__(self):
        self._token_to_entity_ids: Dict[str, Set[int]] = {}
        self._entity_id_to_tokens: Dict[int, List[str]] = {}

    def add(self, entity_id: int, tokens: Tokens):
        """Add an entity to the lookup."""

        assert_entity_id_valid(entity_id)
        assert_tokens_valid(tokens)

        # Store the tokens for the entry
        assert (
            entity_id not in self._entity_id_to_tokens
        ), f"entity {entity_id} already exists"

        self._entity_id_to_tokens[entity_id] = tokens

        # Store the entity ID for the tokens
        for t in tokens:
            if t not in self._token_to_entity_ids:
                self._token_to_entity_ids[t] = set()

            self._token_to_entity_ids[t].add(entity_id)

    def tokens_for_entity(self, entity_id: int) -> Optional[Tokens]:
        """Get tokens for an entity given its ID."""

        assert_entity_id_valid(entity_id)
        return self._entity_id_to_tokens.get(entity_id, None)

    def entity_ids_for_token_list(self, token: str) -> Optional[List[int]]:
        """Get the entity IDs as a list for a given token."""

        assert_token_valid(token)
        if token in self._token_to_entity_ids:
            return sorted(list(self._token_to_entity_ids[token]))
        return None

    def entity_ids_for_token(self, token: str) -> Optional[Set[int]]:
        """Get the entity IDs for a given token."""

        assert_token_valid(token)
        return self._token_to_entity_ids.get(token, None)

    def matching_entries(self, tokens: Tokens) -> Optional[Set[int]]:
        """Find the matching entities in the lookup given the tokens."""

        assert_tokens_valid(tokens)

        # Get the entities for each token
        for idx, t in enumerate(tokens):
            es = self.entity_ids_for_token(t)

            if es is None:
                return None

            if idx == 0:
                entity_ids = es
            else:
                entity_ids = entity_ids.intersection(es)

            # No entries match, so there's no point looking at any further tokens
            if len(entity_ids) == 0:
                return None

        return entity_ids

    def max_number_tokens_for_entity(self) -> int:
        """Maximum number of tokens for an entity."""

        max_num_tokens = 0

        for _, entity_ids in self._token_to_entity_ids.items():
            max_num_tokens = max(max_num_tokens, len(entity_ids))

        return max_num_tokens

    def num_tokens_for_entity(self, entity_id: int) -> Optional[int]:
        """Number of tokens for an entity."""

        tokens = self.tokens_for_entity(entity_id)
        if tokens is None:
            return None

        return len(tokens)
