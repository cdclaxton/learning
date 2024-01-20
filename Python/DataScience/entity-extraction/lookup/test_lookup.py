from .lookup import Lookup


def test_lookup():
    """Unit tests for the Lookup class."""

    l = Lookup()

    # Add an entry
    l.add(0, ["80", "Straight", "Street"])

    assert l.tokens_for_entry(0) == ["80", "Straight", "Street"]
    assert l.tokens_for_entry(1) is None

    assert l.entries_for_token("80") == {0}
    assert l.entries_for_token("Straight") == {0}
    assert l.entries_for_token("Street") == {0}
    assert l.entries_for_token("Road") is None

    # Add a second entry
    l.add(1, ["80", "Broad", "Walk"])
    assert l.tokens_for_entry(0) == ["80", "Straight", "Street"]
    assert l.tokens_for_entry(1) == ["80", "Broad", "Walk"]

    assert l.entries_for_token("80") == {0, 1}
    assert l.entries_for_token("Broad") == {1}


def test_matching_entries():
    """Unit tests for matching_entries()."""

    l = Lookup()
    l.add(0, ["80", "Straight", "Street"])
    l.add(1, ["80", "River", "Street"])
    l.add(2, ["80", "Broad", "Walk"])

    # No matching tokens
    assert l.matching_entries(["Street", "45"]) is None

    # Match one token
    assert l.matching_entries(["80"]) == {0, 1, 2}
    assert l.matching_entries(["Straight"]) == {0}
    assert l.matching_entries(["Street"]) == {0, 1}
    assert l.matching_entries(["Broad"]) == {2}
    assert l.matching_entries(["Walk"]) == {2}

    # Match two tokens
    assert l.matching_entries(["80", "Street"]) == {0, 1}
    assert l.matching_entries(["80", "River"]) == {1}

    # Match three tokens
    assert l.matching_entries(["80", "Street", "Straight"]) == {0}
    assert l.matching_entries(["81", "Street", "Straight"]) is None
