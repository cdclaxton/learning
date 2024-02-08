import pytest
from lookup.token_to_entities_cache import TokenToEntitiesCache


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
