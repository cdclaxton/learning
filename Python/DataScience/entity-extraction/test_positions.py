from positions_compiled_c import calc_positions, PySparsePositionResults


def test_calc_positions():
    """Test calc_positions(), which uses compiled C code."""
    result = calc_positions("|1|2 0|1|32000000".encode(), 32000000, 1)

    expected = PySparsePositionResults(
        n=4,
        error_message="",
    )

    expected.add_result(0, 1, [2])
    expected.add_result(1, 2, [1, 3])
    expected.add_result(2, 1, [2])
    expected.add_result(32000000, 1, [4])

    assert result == expected
