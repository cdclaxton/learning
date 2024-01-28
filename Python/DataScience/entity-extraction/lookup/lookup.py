from typing import Dict, List, Set

from domain import Tokens


class Lookup:
    """Holds two lookups."""

    def __init__(self):
        self._token_to_entity_ids: Dict[str, Set[str]] = {}
        self._entity_id_to_tokens: Dict[str, List[str]] = {}

    def add(self, entity_id: str, tokens: Tokens):
        """Add an entity to the lookup."""
        assert type(entity_id) == str
        assert type(tokens) == list
        assert all([type(t) == str for t in tokens])
        assert len(tokens) > 0

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

    def tokens_for_entity(self, entity_id):
        """Get tokens for an entity given its ID."""

        assert type(entity_id) == str
        return self._entity_id_to_tokens.get(entity_id, None)

    def entity_ids_for_token(self, token):
        """Get the entity IDs for a given token."""

        assert type(token) == str
        return self._token_to_entity_ids.get(token, None)

    def matching_entries(self, tokens):
        """Find the matching entities in the lookup given the tokens."""

        assert type(tokens) == list
        assert all([type(t) == str for t in tokens])
        assert len(tokens) > 0

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
