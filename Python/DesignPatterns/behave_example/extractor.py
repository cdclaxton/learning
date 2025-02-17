import re

simple_postcode = r"[A-Z]{1,2}[0-9]{1,2}\s[0-9][A-Z]{1,2}"


class Extractor:
    def __init__(self):
        self._postcode_regex = re.compile(simple_postcode)

    def postcode(self, text: str) -> None | str:
        """Find the first postcode in the text."""
        m = self._postcode_regex.search(text)
        if m is None:
            return None

        return m[0]
