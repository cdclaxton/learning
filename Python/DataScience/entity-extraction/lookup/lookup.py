from abc import ABC, abstractmethod
from typing import List, Optional, Set

from domain import Tokens


class Lookup(ABC):
    """Abstract base class for a entity and tokens lookup."""

    @abstractmethod
    def add(self, entity_id: str, tokens: Tokens) -> None:
        """Add an entity to the lookup."""
        pass

    @abstractmethod
    def tokens_for_entity(self, entity_id: str) -> Optional[Tokens]:
        """Get tokens for an entity given its ID."""
        pass

    @abstractmethod
    def entity_ids_for_token(self, token: str) -> Optional[Set[str]]:
        """Get the entity IDs for a given token."""
        pass

    @abstractmethod
    def entity_ids_for_token_list(self, token: str) -> Optional[List[str]]:
        """Get the entity IDs as a list for a given token."""
        pass

    @abstractmethod
    def matching_entries(self, tokens: Tokens) -> Optional[Set[str]]:
        """Find the matching entities in the lookup given the tokens."""
        pass

    @abstractmethod
    def max_number_tokens_for_entity(self) -> int:
        """Maximum number of tokens for an entity."""
        pass

    @abstractmethod
    def num_tokens_for_entity(self, entity_id: str) -> Optional[int]:
        """Number of tokens for an entity."""
        pass
