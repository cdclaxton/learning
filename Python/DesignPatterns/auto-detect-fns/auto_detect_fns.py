# This simple Python script demonstrates a way to auto-detect and use functions
# that meet a given naming convention. This could be used as the basis of a
# convention-over-configuration approach.


def wrap_bracket(text):
    """Wrap text in braces."""
    return f"({text})"


def wrap_square_bracket(text):
    """Wrap text in square brackets."""
    return f"[{text}]"


def wrap_stars(text):
    """Wrap text in asterisks."""
    return f"*{text}*"


def auto_detect_functions():
    """Auto-detect functions that start with 'wrap'."""

    # List of functions that match the criteria
    fns = []

    # Walk through the global variables and functions and retain those that
    # start with 'wrap'
    d = globals()
    for name in d:
        if name.startswith("wrap"):
            fns.append(d[name])

    return fns


if __name__ == "__main__":
    # Example text
    text = "Good morning"

    # Get a list of functions by auto-detecting functions that have a given
    # naming convention
    fns = auto_detect_functions()

    # Run the text through each of the auto-detected functions
    for f in fns:
        print(f(text))
