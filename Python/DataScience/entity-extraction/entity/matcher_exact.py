from __future__ import annotations
from collections import deque

from domain import Tokens, assert_token_valid, assert_tokens_valid

from .matcher import EntityMatcher, ProbabilisticMatch
from .sequence import Window

from typing import Dict, List, Optional, Tuple


class Node:
    """Represents a node in a tree data structure."""

    def __init__(self, token: str):
        assert token is None or type(token) == str, f"Got type {type(token)}"

        self._token = token
        self._children = {}  # Map of the token to its node
        self._entity_id: str = None

    def add_child(self, token: str) -> None:
        """Add child node if the token doesn't already exist as a child."""
        assert_token_valid(token)

        if token not in self._children:
            self._children[token] = Node(token)

        return self._children[token]

    def get_child(self, token: str) -> Optional[Node]:
        """Get child node given the token (returns None if child not found)."""
        assert_token_valid(token)

        return self._children.get(token, None)

    def is_leaf(self) -> bool:
        """Is the node a leaf node?"""
        return len(self._children) == 0

    def set_entity_id(self, entity_id: int) -> None:
        """Set the entity ID associated with the node."""
        self._entity_id = entity_id

    def get_entity_id(self) -> int:
        """Get the entity ID associated with the node."""
        return self._entity_id


class Tree:
    """Represents a simple tree data structure."""

    def __init__(self):
        self._root = Node(None)

    def add_tokens(self, tokens: Tokens, entity_id: Optional[int] = None) -> None:
        """Add tokens to the tree (and potentially an entity ID for the last node)."""
        assert_tokens_valid(tokens)
        assert len(tokens) > 0

        if len(tokens) == 1:
            self._root.add_child(tokens[0])
            return

        current_token = self._root.add_child(tokens[0])
        for i in range(1, len(tokens)):
            current_token = current_token.add_child(tokens[i])

        if entity_id is not None:
            current_token.set_entity_id(entity_id)

    def has_tokens(self, tokens: Tokens) -> Tuple[bool, bool, Optional[int]]:
        """Returns whether the tree contains all of the tokens, the final token is a leaf and the entity ID."""
        assert_tokens_valid(tokens)
        assert len(tokens) > 0

        current_node = self._root
        for t in tokens:
            current_node = current_node.get_child(t)
            if current_node is None:
                return False, False, None

        return True, current_node.is_leaf(), current_node.get_entity_id()


def tree_from_entities(entities: Dict[int, Tokens]) -> Tuple[Tree, int]:
    """Returns a Tree for given dict of entities and the max number of tokens."""

    assert type(entities) == dict
    assert all(
        [
            type(entity_id) == int
            and entity_id >= 0
            and type(tokens) == list
            and len(tokens) > 0
            for entity_id, tokens in entities.items()
        ]
    )

    tree = Tree()
    max_num_tokens = 0
    for entity_id, tokens in entities.items():
        tree.add_tokens(tokens, entity_id)
        max_num_tokens = max(len(tokens), max_num_tokens)

    return tree, max_num_tokens


class ExactEntityMatcher(EntityMatcher):
    """Performs an exact entity match."""

    def __init__(self, tree: Tree, max_window_width: int):
        assert type(tree) == Tree
        assert type(max_window_width) == int
        assert max_window_width > 0

        self._tree: Tree = tree
        self._max_window_width: int = max_window_width
        self._window: Window = Window(max_window_width)
        self._matches: List[ProbabilisticMatch] = []

    def reset(self) -> None:
        """Reset the matcher."""
        self._window = Window(self._max_window_width)
        self._matches = []

    def next_token(self, token: str) -> None:
        """Receive the next token in the text."""
        assert_token_valid(token)

        # Adjust the window by adding the token
        self._window.add_token(token)

        # Get the tokens in the window and the absolute start and end indices of
        # the tokens in the text
        tokens_in_window, _, end_idx = self._window.get_tokens()

        for i in range(len(tokens_in_window)):
            tokens_to_check = tokens_in_window[i:]

            # Look for a match
            _, _, entity_id = self._tree.has_tokens(tokens_to_check)

            if entity_id is not None:
                m = ProbabilisticMatch(
                    start=end_idx - len(tokens_to_check) + 1,
                    end=end_idx,
                    entity_id=entity_id,
                    probability=1.0,
                )

                self._matches.append(m)

    def get_matches(self) -> List[ProbabilisticMatch]:
        """Return entity extraction results."""
        return self._matches
