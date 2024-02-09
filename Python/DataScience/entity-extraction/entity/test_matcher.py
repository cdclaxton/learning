from entity.matcher import spans_overlap


def test_spans_overlap():
    # Spans 0 1 2 3 4 5 6 7 8
    # A       ===
    # B           ===
    # C       =====
    # D         ===
    # E               =

    assert not spans_overlap(1, 2, 3, 4)  # A, B
    assert spans_overlap(1, 2, 1, 3)  # A, C
    assert spans_overlap(1, 2, 2, 3)  # A, D
    assert spans_overlap(3, 4, 1, 3)  # B, C
    assert spans_overlap(1, 3, 2, 3)  # C, D
    assert not spans_overlap(1, 2, 5, 5)  # A, E


def test_most_likely_matches():
    pass
