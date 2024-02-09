import pytest
from lookup.token_to_entities_cache import (
    OptimisedTokenToEntitiesCache,
    TokenToEntitiesCache,
    one_more,
)


def test_token_to_entities_cache():
    """Unit tests for TokenToEntitiesCache."""

    cache = TokenToEntitiesCache()

    # Add a token and its entities to the cache
    cache.add("t1", {"e0", "e1"})
    assert "t1" in cache._cache

    # Retain token t1
    cache.retain(["t1"])
    assert "t1" in cache._cache

    # Don't retain t1
    cache.retain(["t2"])
    assert "t2" not in cache._cache

    # Add two tokens and their entities
    cache.add("t1", {"e0", "e1"})
    cache.add("t2", {"e1", "e2", "e3"})

    # Retain both tokens
    cache.retain(["t1", "t2"])
    assert "t1" in cache._cache
    assert "t2" in cache._cache

    # Retain t1, but remove t2
    cache.retain(["t1"])
    assert "t1" in cache._cache
    assert "t2" not in cache._cache

    # Add two tokens and their entities
    # The cache should be:
    # t1: e0, e1
    # t2: e1, e2, e3
    # t3: e3, e4
    cache.add("t2", {"e1", "e2", "e3"})
    cache.add("t3", {"e3", "e4"})

    # Find entities in common
    cache.entities_in_common(["t1"]) == {"e0", "e1"}
    cache.entities_in_common(["t2"]) == {"e1", "e2", "e3"}
    cache.entities_in_common(["t3"]) == {"e3", "e4"}
    cache.entities_in_common(["t1", "t2"]) == {"e1"}
    cache.entities_in_common(["t1", "t3"]) == {}
    cache.entities_in_common(["t2", "t3"]) == {"e3"}
    cache.entities_in_common(["t1", "t2", "t3"]) == {}

    # Find entities in common where a token doesn't exist
    with pytest.raises(Exception):
        cache.entities_in_common(["t4"])

    with pytest.raises(Exception):
        cache.entities_in_common(["t1", "t4"])

    # Tokens required
    cache.required(["t1"]) == []
    cache.required(["t1", "t2"]) == []
    cache.required(["t2", "t3", "t4"]) == ["t4"]
    cache.required(["t5"]) == ["t5"]


def test_token_to_entities_three_entities_in_common():

    cache = TokenToEntitiesCache()

    cache.add("t1", {"e0", "e1"})
    cache.add("t2", {"e0", "e1", "e3"})
    cache.add("t3", {"e0", "e1", "e4"})

    cache.entities_in_common(["t1", "t2", "t3"]) == {"e0", "e1"}


def test_token_to_entities_cache_no_entities():

    cache = TokenToEntitiesCache()

    # Add a token and its entities to the cache
    cache.add("t1", {"e0", "e1"})
    assert "t1" in cache._cache

    # Add a token that doesn't have any matching entities
    cache.add("t2", None)
    assert "t2" in cache._cache

    # Find entities in common
    cache.entities_in_common(["t1"]) == {"e0", "e1"}
    cache.entities_in_common(["t2"]) == {}
    cache.entities_in_common(["t1", "t2"]) == {}


def test_one_more():
    """Unit tests for one_more()."""

    assert one_more(set(), {"a"}) == (True, "a")
    assert one_more({"a"}, {"a", "b"}) == (True, "b")
    assert one_more({"a", "b"}, {"a", "b", "c"}) == (True, "c")
    assert one_more({"a", "b", "c"}, {"a", "b", "c", "d"}) == (True, "d")

    assert one_more({"a"}, {"a"}) == (False, None)
    assert one_more({"a"}, {"b"}) == (False, None)
    assert one_more({"a", "b"}, {"b"}) == (False, None)
    assert one_more({"a", "b"}, {"a", "b"}) == (False, None)
    assert one_more({"a", "b"}, {"a", "d"}) == (False, None)
    assert one_more({"a", "b", "c"}, {"a", "d", "e"}) == (False, None)


def test_optimised_token_to_entities_cache():

    # Map of token to entity IDs
    token_to_entity_ids = {
        "a": {"e0"},
        "b": {"e0", "e1"},
        "c": {"e0", "e2"},
        "d": {"e3"},
    }

    def entity_getter(entity):
        return token_to_entity_ids.get(entity, None)

    cache = OptimisedTokenToEntitiesCache(entity_getter)

    # Get entities for a single token
    cache.get(["a"]) == ({"e0"}, False)
    cache.get(["b"]) == ({"e0", "e1"}, False)

    # Check tokens [a] -> [a,b] -> [a,b,c]
    cache.clear()
    cache.get(["a"]) == ({"e0"}, False)
    cache.get(["a", "b"]) == ({"e0"}, True)
    cache.get(["a", "b", "c"]) == ({"e0"}, True)

    # Check tokens [a] -> [a,d] -> [a,d,b]
    cache.clear()
    cache.get(["a"]) == ({"e0"}, False)
    cache.get(["a", "d"]) == ({}, True)
    cache.get(["a", "d", "b"]) == ({}, True)

    # Check tokens [a] -> [a, e] -> [a, e, b]
    cache.clear()
    cache.get(["a"]) == ({"e0"}, False)
    cache.get(["a", "e"]) == ({}, True)
    cache.get(["a", "e", "b"]) == ({}, True)
