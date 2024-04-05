import string
from typing import Optional
from domain import Tokens
from nltk.tokenize import wordpunct_tokenize


def tokenise_text(text: str) -> Optional[Tokens]:
    """Tokenise the text into tokens and make each token lowercase."""

    if type(text) != str:
        return None

    if len(text) == 0:
        return None

    punct = set(string.punctuation)

    def only_punctuation(text: str) -> bool:
        """Is the text composed of just punctuation?"""
        return all([t in punct for t in text])

    # Tokenise the lowercase version of the text
    tokens = wordpunct_tokenize(text.lower())

    # Remove tokens that are only punctuation
    return [t for t in tokens if not only_punctuation(t)]
