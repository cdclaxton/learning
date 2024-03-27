# Suppose the data comes in the form:
# <ID> <ID>|<ID> <ID> <ID>|<ID> ...
# where a space separates IDs for a given index and the pipe denotes a new
# index.

from typing import Any, Dict, List


def split(s: str) -> List[List[int]]:

    result = []

    batch = []

    start = 0
    end = 0

    while end < len(s):
        if s[end] == " ":
            batch.append(int(s[start:end]))
            start = end + 1

        elif s[end] == "|":
            batch.append(int(s[start:end]))
            result.append(batch)
            batch = []
            start = end + 1

        end += 1

    if start != end:
        batch.append(int(s[start:end]))

    if len(batch) > 0:
        result.append(batch)

    return result


if __name__ == "__main__":

    test_cases: List[Dict[str, Any]] = [
        {"text": "1", "expected": [[1]]},
        {"text": "1 2", "expected": [[1, 2]]},
        {"text": "1 2 3", "expected": [[1, 2, 3]]},
        {"text": "1|2", "expected": [[1], [2]]},
        {"text": "1 2|3", "expected": [[1, 2], [3]]},
        {"text": "1 2|3 4", "expected": [[1, 2], [3, 4]]},
        {"text": "1 2|3|4 5", "expected": [[1, 2], [3], [4, 5]]},
    ]

    for idx, test_case in enumerate(test_cases):
        result = split(test_case["text"])
        assert (
            result == test_case["expected"]
        ), f"Expected {test_case['expected']}, got {result}"
