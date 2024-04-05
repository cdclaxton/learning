# cython: language_level=3

from typing import List, Tuple

def adds_removes_from_positions(
    pos: List[int],
    n_entity_tokens: int,
    min_window: int,
    max_window: int,
) -> List[Tuple[int, int, int, int]]:
    """Calculate the number of tokens added and removed given the positions."""


    result: List[Tuple[int, int, int, int]] = []
    if len(pos) == 0:
        return result
    elif len(pos) == 1:
        result.append((pos[0], pos[0], 0, n_entity_tokens-1))

    for i in range(0, len(pos) - 1):
        for j in range(i + 1, len(pos)):

            # Number of text tokens
            n_t = pos[j] - pos[i] + 1

            if n_t < min_window:
                continue
            elif n_t > max_window:
                break

            # Number of tokens in common (in text and entity)
            n_c = j - i + 1

            # Number of tokens added
            n_adds = max(0, n_t - n_c)

            # Number of tokens remvoed
            n_removes = max(0, n_entity_tokens - n_c)

            result.append((pos[i], pos[j], n_adds, n_removes))

    return result
