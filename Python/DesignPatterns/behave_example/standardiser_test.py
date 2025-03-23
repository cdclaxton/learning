from standardiser import standardise_sortcode


def test_sortcode_standardiser():
    assert standardise_sortcode("102030") == "102030"
    assert standardise_sortcode("10 50 70") == "105070"
    assert standardise_sortcode("10-50-80") == "105080"
    assert standardise_sortcode("  20-30-40") == "203040"
    assert standardise_sortcode("  20-30-50  ") == "203050"
