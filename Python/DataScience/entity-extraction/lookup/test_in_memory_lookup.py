from lookup.in_memory_lookup import InMemoryLookup


def test_lookup():
    """Unit tests for the Lookup class."""

    l = InMemoryLookup()

    # Add an entry
    l.add("e-0", ["80", "Straight", "Street"])

    assert l.tokens_for_entity("e-0") == ["80", "Straight", "Street"]
    assert l.tokens_for_entity("e-1") is None

    assert l.entity_ids_for_token("80") == {"e-0"}
    assert l.entity_ids_for_token("Straight") == {"e-0"}
    assert l.entity_ids_for_token("Street") == {"e-0"}
    assert l.entity_ids_for_token("Road") is None

    assert l.entity_ids_for_token_list("80") == ["e-0"]
    assert l.entity_ids_for_token_list("Road") is None

    # Add a second entry
    l.add("e-1", ["80", "Broad", "Walk"])
    assert l.tokens_for_entity("e-0") == ["80", "Straight", "Street"]
    assert l.tokens_for_entity("e-1") == ["80", "Broad", "Walk"]

    assert l.entity_ids_for_token("80") == {"e-0", "e-1"}
    assert l.entity_ids_for_token("Broad") == {"e-1"}


def test_matching_entries():
    """Unit tests for matching_entries()."""

    l = InMemoryLookup()
    l.add("e-0", ["80", "Straight", "Street"])
    l.add("e-1", ["80", "River", "Street"])
    l.add("e-2", ["80", "Broad", "Walk"])

    # No matching tokens
    assert l.matching_entries(["Street", "45"]) is None

    # Match one token
    assert l.matching_entries(["80"]) == {"e-0", "e-1", "e-2"}
    assert l.matching_entries(["Straight"]) == {"e-0"}
    assert l.matching_entries(["Street"]) == {"e-0", "e-1"}
    assert l.matching_entries(["Broad"]) == {"e-2"}
    assert l.matching_entries(["Walk"]) == {"e-2"}

    # Match two tokens
    assert l.matching_entries(["80", "Street"]) == {"e-0", "e-1"}
    assert l.matching_entries(["80", "River"]) == {"e-1"}

    # Match three tokens
    assert l.matching_entries(["80", "Street", "Straight"]) == {"e-0"}
    assert l.matching_entries(["81", "Street", "Straight"]) is None
