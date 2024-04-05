from abc import ABC, abstractmethod
from typing import List, Optional, Set

from domain import Tokens


class Lookup(ABC):
    """Abstract base class for a entity and tokens lookup."""

    @abstractmethod
    def add(
        self, internal_entity_id: int, external_entity_id: str, tokens: Tokens
    ) -> None:
        """Add an entity to the lookup."""
        pass

    @abstractmethod
    def tokens_for_entity(self, internal_entity_id: int) -> Optional[Tokens]:
        """Get tokens for an entity given its internal ID."""
        pass

    @abstractmethod
    def entity_ids_for_token(self, token: str) -> Optional[Set[int]]:
        """Get the internal entity IDs for a given token."""
        pass

    @abstractmethod
    def entity_ids_for_token_list(self, token: str) -> Optional[List[int]]:
        """Get the internal entity IDs as a list for a given token."""
        pass

    @abstractmethod
    def entity_ids_for_token_string(self, token: str) -> Optional[str]:
        """Get the internal entity IDs as a string for a given token."""
        pass

    @abstractmethod
    def matching_entries(self, tokens: Tokens) -> Optional[Set[int]]:
        """Find the matching internal entities in the lookup given the tokens."""
        pass

    @abstractmethod
    def max_number_tokens_for_entity(self) -> int:
        """Maximum number of tokens for an entity."""
        pass

    @abstractmethod
    def num_tokens_for_entity(self, internal_entity_id: int) -> Optional[int]:
        """Number of tokens for an entity given its internal ID."""
        pass

    @abstractmethod
    def max_entity_id(self) -> int:
        """Maximum internal entity ID."""
        pass

    @abstractmethod
    def external_entity_id(self, internal_entity_id: int) -> Optional[str]:
        """Get the external entity ID given its internal ID."""
        pass
