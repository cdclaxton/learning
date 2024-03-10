from .matcher_exact import *


def test_node():
    """Unit tests for the Node class."""

    # Make a root node
    root = Node("t")
    assert root.get_child("h") is None
    assert root.is_leaf()
    assert root.get_entity_id() is None

    # Set the entity ID of the root node
    root.set_entity_id(100)
    assert root.get_entity_id() == 100

    # Add a leaf node
    node_h = root.add_child("h")
    assert node_h is not None
    assert root.get_child("h") is not None
    assert not root.is_leaf()
    assert node_h.is_leaf()

    # Check entity IDs
    assert root.get_entity_id() == 100
    assert node_h.get_entity_id() is None

    # Set the leaf node's entity ID
    node_h.set_entity_id(200)
    assert root.get_entity_id() == 100
    assert node_h.get_entity_id() == 200


def test_tree():
    """Unit tests for the Tree class."""
    tree = Tree()
    assert tree.has_tokens(["a"]) == (False, False, None)

    # Add tokens for an entity 'a'
    tree.add_tokens(["a"])
    assert tree.has_tokens(["t"]) == (False, False, None)
    assert tree.has_tokens(["a"]) == (True, True, None)

    # Add tokens for an entity 'abc'
    tree.add_tokens(["a", "b", "c"], "entity-1")
    assert tree.has_tokens(["a", "b"]) == (True, False, None)
    assert tree.has_tokens(["a", "b", "c"]) == (True, True, "entity-1")
    assert tree.has_tokens(["a", "b", "d"]) == (False, False, None)

    # Add tokens for an entity 'abcd'
    tree.add_tokens(["a", "b", "c", "d"], "entity-2")
    assert tree.has_tokens(["a", "b"]) == (True, False, None)
    assert tree.has_tokens(["a", "b", "c"]) == (True, False, "entity-1")
    assert tree.has_tokens(["a", "b", "c", "d"]) == (True, True, "entity-2")

    # Add tokens for another entity
    tree.add_tokens(["a", "b", "d", "e"])
    assert tree.has_tokens(["a", "b", "d", "e"]) == (True, True, None)
    assert tree.has_tokens(["a", "b", "d", "e", "f"]) == (False, False, None)


def add_token_check(matcher, token, expected):
    """Add a token to the matcher and check the result."""
    matcher.next_token(token)
    actual = matcher.get_matches()
    assert expected == actual, f"expected: {expected}, got: {actual}"


def test_exact_entity_matcher():
    """Unit tests for ExactEntityMatcher."""

    # Tree for detecting entities
    tree, window_size = tree_from_entities(
        {
            1: "a b".split(),
            2: "a b c".split(),
            3: "d e".split(),
        }
    )

    assert tree.has_tokens(["a"]) == (True, False, None)
    assert tree.has_tokens(["a", "b"]) == (True, False, 1)
    assert tree.has_tokens(["a", "b", "c"]) == (True, True, 2)
    assert tree.has_tokens(["d"]) == (True, False, None)
    assert tree.has_tokens(["d", "e"]) == (True, True, 3)
    assert tree.has_tokens(["f"]) == (False, False, None)

    matcher = ExactEntityMatcher(tree, window_size)

    # Index:    0 1 2
    # Tokens:   a b e
    # Matches:  ===    <-- e-1
    m1 = ProbabilisticMatch(0, 1, 1, 1.0)
    add_token_check(matcher, "a", [])
    add_token_check(matcher, "b", [m1])
    add_token_check(matcher, "e", [m1])

    # Index:    0 1 2
    # Tokens:   a b c
    # Matches:  ===    <-- e-1
    #           =====  <-- e-2
    matcher.reset()
    m1 = ProbabilisticMatch(0, 1, 1, 1.0)
    m2 = ProbabilisticMatch(0, 2, 2, 1.0)
    add_token_check(matcher, "a", [])
    add_token_check(matcher, "b", [m1])
    add_token_check(matcher, "c", [m1, m2])

    # Index:    0 1 2 3 4
    # Tokens:   f d e c g
    # Matches:    ===      <-- e-3
    matcher.reset()
    m1 = ProbabilisticMatch(1, 2, 3, 1.0)
    add_token_check(matcher, "f", [])
    add_token_check(matcher, "d", [])
    add_token_check(matcher, "e", [m1])
    add_token_check(matcher, "c", [m1])
    add_token_check(matcher, "g", [m1])

    # Index:    0 1 2 3 4 5
    # Tokens:   f d e a b c
    # Matches:    ===        <-- e-3
    #                 ===    <-- e-1
    #                 =====  <-- e-2
    matcher.reset()
    m1 = ProbabilisticMatch(1, 2, 3, 1.0)
    m2 = ProbabilisticMatch(3, 4, 1, 1.0)
    m3 = ProbabilisticMatch(3, 5, 2, 1.0)
    add_token_check(matcher, "f", [])
    add_token_check(matcher, "d", [])
    add_token_check(matcher, "e", [m1])
    add_token_check(matcher, "a", [m1])
    add_token_check(matcher, "b", [m1, m2])
    add_token_check(matcher, "c", [m1, m2, m3])
