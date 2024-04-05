from text.tokeniser import tokenise_text


def test_tokenise_text():
    """Unit tests for tokenise_text()."""

    test_cases = [
        {"text": 1234, "expected": None},
        {"text": "", "expected": None},
        {"text": "This is an example.", "expected": ["this", "is", "an", "example"]},
        {"text": "This-is a test", "expected": ["this", "is", "a", "test"]},
        {"text": "Test 1. Test 2.", "expected": ["test", "1", "test", "2"]},
        {"text": "Test 1..Test 2.", "expected": ["test", "1", "test", "2"]},
    ]

    for test_case in test_cases:
        actual = tokenise_text(test_case["text"])
        assert (
            actual == test_case["expected"]
        ), f"Error tokenising {test_case['text']}, expected: {test_case['expected']}, actual: {actual}"
