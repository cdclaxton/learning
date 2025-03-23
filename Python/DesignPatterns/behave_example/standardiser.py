import re

standardised_sortcode = re.compile(r"^[0-9]{6}$")
sortcode_pattern = re.compile(r"^([0-9]{2})[\s-]?([0-9]{2})[\s-]?([0-9]{2})$")


# Simple sort-code standardiser
def standardise_sortcode(text):

    # Remove leading and trailing whitespace
    text = text.strip()

    # Is the sortcode already in a standardised form?
    if standardised_sortcode.match(text):
        return text

    # Try to match the parts of the sort-code
    matches = sortcode_pattern.match(text)
    if matches is None:
        return None

    return f"{matches[1]}{matches[2]}{matches[3]}"
