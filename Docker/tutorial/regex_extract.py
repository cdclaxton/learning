# This Python script extracts sort-codes and account numbers from free-text.
import re

# Regular expression to extract a sort-code account number pair
pattern = r"([0-9]{2}-[0-9]{2}-[0-9]{2})\s+([0-9]{8})"

# Compile the regular expression for speed
compiled = re.compile(pattern=pattern)

# Fields in the returned dict
sortcode_field = "sortcode"
account_field = "account"


def extract(text):
    """Extract sort-codes and account numbers from free text."""

    # Preconditions
    assert type(text) == str

    # Run the regular expression over the text
    result = compiled.findall(text)

    # Return a list of a dicts
    return [{sortcode_field: r[0], account_field: r[1]} for r in result]
