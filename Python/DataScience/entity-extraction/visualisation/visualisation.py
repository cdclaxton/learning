from typing import Dict, List, Tuple
from domain import Tokens, assert_probability_valid, assert_tokens_valid
from entity.matcher import ProbabilisticMatch


def pad(value: str, width: int) -> str:
    """Pad a string with spaces to meet a required width."""
    assert type(value) == str
    assert type(width) == int
    assert len(value) <= width

    num_spaces = width - len(value)
    return value + " " * num_spaces


class TextTable:
    def __init__(self, n_rows: int, n_cols: int):
        """Instantiate a text table with n_rows and n_cols."""
        assert type(n_rows) == int and n_rows > 0
        assert type(n_cols) == int and n_cols > 0

        self._n_rows = n_rows
        self._n_cols = n_cols
        self._table = [["" for _ in range(n_cols)] for _ in range(n_rows)]

    def cell(self, row: int, col: int, value: str) -> None:
        """Set the value in a cell."""
        assert type(row) == int and 0 <= row < self._n_rows
        assert type(col) == int and 0 <= col < self._n_cols

        self._table[row][col] = value

    def cells(self, data: List[Tuple[int, int, str]]) -> None:
        """Set the values in multiple cells."""

        for row, col, value in data:
            self.cell(row, col, value)

    def _calc_column_widths(self) -> List[int]:
        """Calculate the widths of each column."""

        column_widths: List[int] = [0 for _ in range(self._n_cols)]

        for row in self._table:
            for col_idx, value in enumerate(row):
                column_widths[col_idx] = max(column_widths[col_idx], len(value))

        return column_widths

    def _build_row(self, row: List[str], column_widths: List[int]) -> str:
        """Build a single row of the table."""

        assert len(row) == len(column_widths)

        result = ""
        for col_idx, cell_value in enumerate(row):
            result += pad(cell_value, column_widths[col_idx])
            if col_idx < self._n_cols - 1:
                result += " "

        return result

    def build(self) -> str:
        """Build the table."""

        # Find the required width of each column
        column_widths = self._calc_column_widths()

        result = ""
        for row in self._table:
            result += self._build_row(row, column_widths) + "\n"

        return result


def format_probability(prob: float) -> str:
    return f"{prob:.3f}"


def format_entity(tokens: Tokens) -> str:
    """Format the tokens for an entity."""
    assert_tokens_valid(tokens)
    return " ".join(tokens)


def visualise_probabilistic_matches(
    text_tokens: Tokens,
    matches: List[ProbabilisticMatch],
    entity_id_to_tokens: Dict[str, Tokens],
) -> str:
    """Visualise probabilistic matches."""

    assert_tokens_valid(text_tokens)
    assert type(matches) == list
    assert type(entity_id_to_tokens) == dict

    # Number of columns in the table (two extra for the probability and the
    # matching entity)
    n_cols = len(text_tokens) + 2

    # Number of rows
    n_rows = len(matches) + 1

    # Build the text table
    tt = TextTable(n_rows, n_cols)

    # Add the tokens
    for idx, token in enumerate(text_tokens):
        tt.cell(0, idx, token)

    # Get the column widths for the tokens
    column_widths: List[int] = tt._calc_column_widths()

    # Add each of the matches
    row_offset = 1
    prob_col = len(text_tokens)
    entity_col = prob_col + 1
    for match_idx, match in enumerate(matches):
        assert type(match) == ProbabilisticMatch

        # Draw a symbol to show the entity span
        for col_idx in range(match.start, match.end + 1):
            assert col_idx < len(
                column_widths
            ), f"got token match position {col_idx}, but there are {len(text_tokens)} tokens"
            symb = "=" * column_widths[col_idx]
            tt.cell(row_offset + match_idx, col_idx, symb)

        # Show the probability
        tt.cell(row_offset + match_idx, prob_col, format_probability(match.probability))

        # Show the matched entity
        entity_id = match.entity_id
        assert entity_id in entity_id_to_tokens
        tt.cell(
            row_offset + match_idx,
            entity_col,
            format_entity(entity_id_to_tokens[entity_id]),
        )

    return tt.build()


def visualise_probabilistic_matches_over_threshold(
    text_tokens: Tokens,
    matches: List[ProbabilisticMatch],
    entity_id_to_tokens: Dict[str, Tokens],
    threshold: float,
) -> str:
    """Visualise probabilistic matches over a given threshold."""

    assert_probability_valid(threshold)

    # Retain matches that at or exceed the threshold
    filtered_matches = [m for m in matches if m.probability >= threshold]

    # Sort the matches by their probability
    sorted_filtered_matches = sorted(
        filtered_matches, key=lambda x: x.probability, reverse=True
    )

    return visualise_probabilistic_matches(
        text_tokens, sorted_filtered_matches, entity_id_to_tokens
    )
