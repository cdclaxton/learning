from entity.matcher_add_remove import (
    EntityMatcherAddRemove,
    adds_removes_from_positions,
    subdivide_text,
)
from likelihood.likelihood_add_remove import make_likelihood_add_remove_symmetric
from lookup.in_memory_lookup import InMemoryLookup
from text.tokeniser import tokenise_text


def test_adds_removes_from_positions():
    """Unit tests for adds_removes_from_positions()."""

    # No adds, no removes
    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Matching:      * * *
    assert adds_removes_from_positions([0, 1, 2], 3, 3, 3) == [(0, 2, 0, 0)]

    # No adds, no removes
    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Matching:        * * *
    assert adds_removes_from_positions([1, 2, 3], 3, 3, 3) == [(1, 3, 0, 0)]

    # One add, one remove
    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Matching:        * *   *
    assert adds_removes_from_positions([1, 2, 4], 4, 4, 4) == [(1, 4, 1, 1)]

    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Matching:        * *   * *
    # Window 0:        =======
    # Window 1:          =====
    # Window 2:          =======
    assert adds_removes_from_positions([1, 2, 4, 5], 3, 3, 4) == [
        (1, 4, 1, 0),
        (2, 4, 1, 1),
        (2, 5, 1, 0),
    ]


def test_subdivide_test():
    """Unit tests for subdivide_text()."""

    # Text fits within a single segment
    assert subdivide_text(8, 10, 5) == [(0, 8)]
    assert subdivide_text(10, 10, 5) == [(0, 10)]

    # Text spans two segments
    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Segment 0:     =====
    # Segment 1:       =====
    assert subdivide_text(4, 3, 3) == [(0, 3), (1, 4)]

    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Segment 0:     =====
    # Segment 1:         =====
    assert subdivide_text(5, 3, 2) == [(0, 3), (2, 5)]

    # Text spans two segments
    # Token index:   0 1 2 3 4 5 6 7 8 9 10
    # Segment 0:     =========
    # Segment 1:           =========
    # Segment 2:                 =======
    assert subdivide_text(10, 5, 3) == [(0, 5), (3, 8), (6, 10)]


def test_matcher_add_remove():

    # Create an in-memory lookup
    lookup = InMemoryLookup()

    # Add the entities to the lookup
    entities = [
        (0, "100", "78 Straight Street London"),
        (1, "101", "6 The Walk London"),
        (2, "102", "10 The Mews Birmingham"),
        (3, "103", "12 The Mews Birmingham"),
    ]

    for internal_id, external_id, text in entities:
        tokens = tokenise_text(text)
        assert tokens is not None
        lookup.add(internal_id, external_id, tokens)

    # Make a simple likelihood function
    likelihood_symmetric = make_likelihood_add_remove_symmetric(0.2, 0.9, 0.5, 0.1)

    # Instantiate the entity matcher
    matcher = EntityMatcherAddRemove(
        lookup=lookup,
        likelihood=likelihood_symmetric,
        min_window=2,
        max_window=5,
        min_probability=0.8,
        max_entity_id=3,
    )

    for start_idx in range(240, 260):

        tokens = ["a" for _ in range(start_idx)]
        tokens.extend(["78", "straight", "street", "london"])
        tokens.extend(["b" for _ in range(20)])

        for t in tokens:
            matcher.next_token(t)

        matches = matcher.get_matches()

        assert len(matches) == 1
        assert matches[0].entity_id == 0
        assert matches[0].start == start_idx
        assert matches[0].end == matches[0].start + 3

        matcher.reset()
