def markdown_row(elements):
    """Returns a row of Markdown formatted elements."""

    assert type(elements) == list
    return "| " + " | ".join(elements) + " |"
