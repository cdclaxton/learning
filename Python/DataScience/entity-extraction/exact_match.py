# This script explores how to find exact matches in an efficient manner.
from dataclasses import dataclass


class Node:
    """Represents a node in a tree data structure."""

    def __init__(self, token):
        assert token is None or type(token) == str, f"Got type {type(token)}"
        self.token = token
        self.children = {}  # Map of the token to its node

    def add_child(self, token):
        """Add child node if the token doesn't already exist as a child."""
        assert type(token) == str
        if token not in self.children:
            self.children[token] = Node(token)

        return self.children[token]

    def get_child(self, token):
        """Get child node given the token (returns None if child not found)."""
        assert type(token) == str
        return self.children.get(token, None)

    def is_leaf(self):
        """Is the node a leaf node?"""
        return len(self.children) == 0


def test_node():
    """Unit tests for the Node class."""
    root = Node("t")
    assert root.get_child("h") is None
    assert root.is_leaf()

    node_h = root.add_child("h")
    assert node_h is not None
    assert root.get_child("h") is not None
    assert not root.is_leaf()
    assert node_h.is_leaf()


class Tree:
    def __init__(self):
        self.root = Node(None)

    def add_tokens(self, tokens):
        assert type(tokens) == list
        assert len(tokens) > 0

        if len(tokens) == 1:
            self.root.add_child(tokens[0])
            return

        current_token = self.root.add_child(tokens[0])
        for i in range(1, len(tokens)):
            current_token = current_token.add_child(tokens[i])

    def has_tokens(self, tokens):
        assert type(tokens) == list
        assert len(tokens) > 0

        current_node = self.root
        for t in tokens:
            current_node = current_node.get_child(t)
            if current_node is None:
                return False, False

        return True, current_node.is_leaf()


def test_tree():
    """Unit tests for the Tree class."""
    tree = Tree()
    assert tree.has_tokens(["a"]) == (False, False)

    tree.add_tokens(["a"])
    assert tree.has_tokens(["t"]) == (False, False)
    assert tree.has_tokens(["a"]) == (True, True)

    tree.add_tokens(["a", "b", "c"])
    tree.add_tokens(["a", "b", "d", "e"])
    assert tree.has_tokens(["a", "b"]) == (True, False)
    assert tree.has_tokens(["a", "b", "c"]) == (True, True)
    assert tree.has_tokens(["a", "b", "d"]) == (True, False)
    assert tree.has_tokens(["a", "b", "d", "e"]) == (True, True)
    assert tree.has_tokens(["a", "b", "d", "e", "f"]) == (False, False)


class TokenMatch:
    """Represents where tokens match in a list of tokens."""

    def __init__(self, start_index: int, length: int):
        assert start_index >= 0, f"Invalid start index: {start_index}"
        assert length > 0, f"Invalid length: {length}"

        self.start_index = start_index
        self.length = length

    def __eq__(self, other):
        if not isinstance(other, TokenMatch):
            return False

        return self.start_index == other.start_index and self.length == other.length

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(start={self.start_index}, length={self.length})"

    def __str__(self) -> str:
        return self.__repr__()


def test_token_match():
    """Unit tests for TokenMatch."""

    t1 = TokenMatch(0, 2)
    t2 = TokenMatch(0, 2)
    t3 = TokenMatch(1, 2)

    assert t1 == t2
    assert t1 != t3


def find_matches(tree, tokens):
    """Find matches in the tokens given a tree of tokens to find."""

    assert type(tree) == Tree
    assert type(tokens) == list
    assert all([type(t) == str for t in tokens])

    matches = []

    for start_idx in range(0, len(tokens)):
        match, leaf = tree.has_tokens([tokens[start_idx]])

        if not match:
            continue

        if leaf:
            matches.append(TokenMatch(start_idx, 1))

        for span_idx in range(start_idx + 1, len(tokens)):
            match, leaf = tree.has_tokens(tokens[start_idx : (span_idx + 1)])

            if not match:
                break

            if leaf:
                length = span_idx - start_idx + 1
                matches.append(TokenMatch(start_idx, length))

    if len(matches) == 0:
        matches = None

    return matches


def test_find_matches():
    # Make a tree that holds:
    #
    #     /--> a -> b -> c
    # root           \--> d -> e -> e
    #     \
    #      \--> b -> c
    #       \
    #        \--> e
    # Note that the sequence [b, c] exists as part of [a, b, c] and on its own.

    tree = Tree()
    tree.add_tokens(["a", "b", "c"])
    tree.add_tokens(["a", "b", "d", "e", "e"])
    tree.add_tokens(["b", "c"])
    tree.add_tokens(["e"])

    # No match
    assert find_matches(tree, ["x", "y"]) is None

    # No match (just partial)
    assert find_matches(tree, ["a"]) is None
    assert find_matches(tree, ["a", "b"]) is None
    assert find_matches(tree, ["a", "b", "d", "f"]) is None
    assert find_matches(tree, ["b"]) is None

    # Full match (matches all tokens)
    assert find_matches(tree, ["b", "c"]) == [TokenMatch(0, 2)]
    assert find_matches(tree, ["a", "b", "c"]) == [TokenMatch(0, 3), TokenMatch(1, 2)]
    assert find_matches(tree, ["a", "b", "d", "e", "e"]) == [
        TokenMatch(0, 5),
        TokenMatch(3, 1),
        TokenMatch(4, 1),
    ]
    assert find_matches(tree, ["e"]) == [TokenMatch(0, 1)]

    # Full, single match with surrounding tokens
    assert find_matches(tree, ["x", "b", "c"]) == [TokenMatch(1, 2)]
    assert find_matches(tree, ["x", "b", "c", "y"]) == [TokenMatch(1, 2)]
    assert find_matches(tree, ["x", "y", "b", "c", "z"]) == [TokenMatch(2, 2)]
    assert find_matches(tree, ["x", "y", "a", "b", "c"]) == [
        TokenMatch(2, 3),
        TokenMatch(3, 2),
    ]

    assert find_matches(tree, ["x", "a", "b", "d", "e", "e", "z"]) == [
        TokenMatch(1, 5),
        TokenMatch(4, 1),
        TokenMatch(5, 1),
    ]
    assert find_matches(tree, ["e", "x"]) == [TokenMatch(0, 1)]
    assert find_matches(tree, ["x", "e"]) == [TokenMatch(1, 1)]

    # Multiple matches
    assert find_matches(tree, ["e", "b", "c"]) == [TokenMatch(0, 1), TokenMatch(1, 2)]
    assert find_matches(tree, ["e", "x", "b", "c"]) == [
        TokenMatch(0, 1),
        TokenMatch(2, 2),
    ]


if __name__ == "__main__":
    # Run unit tests
    test_node()
    test_tree()
    test_token_match()
    test_find_matches()
