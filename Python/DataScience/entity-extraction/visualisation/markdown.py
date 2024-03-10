from typing import List


def markdown_row(elements: List[str]):
    """Returns a row of Markdown formatted elements."""

    assert type(elements) == list
    return "| " + " | ".join(elements) + " |"
