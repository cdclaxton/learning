from entity.matcher import ProbabilisticMatch
from visualisation.visualisation import TextTable, pad, visualise_probabilistic_matches


def test_text_table():
    tt = TextTable(3, 4)

    # Create the table:
    # Row \ Col 0  1  2     3
    #   0       A  BB  C    J
    #   1       DD E   FFF  K
    #   2       G  HHH IIII LL

    tt.cells(
        [
            (0, 0, "A"),
            (0, 1, "BB"),
            (0, 2, "C"),
            (0, 3, "J"),
            (1, 0, "DD"),
            (1, 1, "E"),
            (1, 2, "FFF"),
            (1, 3, "K"),
            (2, 0, "G"),
            (2, 1, "HHH"),
            (2, 2, "IIII"),
            (2, 3, "LL"),
        ]
    )

    assert tt._calc_column_widths() == [2, 3, 4, 2]

    expected = "A  BB  C    J \nDD E   FFF  K \nG  HHH IIII LL\n"
    assert tt.build() == expected


def test_text_table_pad():
    assert pad("", 1) == " "
    assert pad("", 2) == "  "
    assert pad("a", 1) == "a"
    assert pad("a", 2) == "a "
    assert pad("a", 3) == "a  "
    assert pad("ab", 2) == "ab"
    assert pad("ab", 3) == "ab "


def test_visualise_probabilistic_matches():
    text_tokens = ["A", "BB", "CCC"]
    matches = [
        ProbabilisticMatch(0, 0, "e-1", 0.99),
        ProbabilisticMatch(0, 1, "e-1", 0.80),
        ProbabilisticMatch(0, 2, "e-1", 0.75),
        ProbabilisticMatch(1, 1, "e-2", 0.60),
        ProbabilisticMatch(1, 2, "e-2", 0.59),
        ProbabilisticMatch(2, 2, "e-3", 0.04),
    ]
    entity_id_to_tokens = {"e-1": "F G H".split(), "e-2": "J K".split(), "e-3": ["L"]}

    result = visualise_probabilistic_matches(text_tokens, matches, entity_id_to_tokens)
    assert type(result) == str
