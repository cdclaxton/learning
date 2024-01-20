from collections import deque
from typing import Deque, List, Any, Tuple


def correct_sequence(entity_tokens: List[Any], text_tokens: List[Any]):
    """Are the tokens in the text in the correct order for the entity?"""

    assert type(entity_tokens) == list
    assert len(entity_tokens) > 0
    assert type(text_tokens) == list
    assert len(text_tokens) > 0

    if len(text_tokens) > len(entity_tokens):
        return False

    text_token_index = 0
    for entity_token in entity_tokens:
        if entity_token == text_tokens[text_token_index]:
            text_token_index += 1
            if text_token_index == len(text_tokens):
                break

    return text_token_index == len(text_tokens)


class Window:
    """Represents a window of tokens in a text."""

    def __init__(self, max_window_size: int):
        assert type(max_window_size) == int
        assert max_window_size > 0

        self.max_window_size: int = max_window_size
        self.tokens: Deque = deque()
        self.current_token_index: int = -1

    def add_token(self, token: Any) -> None:
        """Add a token to the window."""

        self.current_token_index += 1

        # Store the new token
        self.tokens.append(token)

        # Remove the older elements to retain the required window size
        while len(self.tokens) > self.max_window_size:
            self.tokens.popleft()

    def get_tokens(self) -> Tuple[List[Any], int, int]:
        """Get tokens in the window and the indices of the first and last element."""

        return (
            list(self.tokens),
            max(0, self.current_token_index - len(self) + 1),  # index of first element
            self.current_token_index,  # index of last element
        )

    def __len__(self) -> int:
        """Length of the current window."""
        return len(self.tokens)
