import typing
from .sequence import correct_sequence, Window


def test_correct_sequence():
    """Unit tests for correct_sequence()."""

    # Too many tokens in text for the likelihood function
    assert not correct_sequence(["A"], ["A", "B"])
    assert not correct_sequence(["A", "B"], ["A", "B", "C"])

    # Correct number of tokens, none missing
    assert correct_sequence(["A"], ["A"])
    assert correct_sequence(["A", "B"], ["A", "B"])
    assert correct_sequence(["A", "B", "C"], ["A", "B", "C"])

    # One missing token
    assert correct_sequence(["A", "B"], ["A"])
    assert correct_sequence(["A", "B"], ["B"])
    assert correct_sequence(["A", "B", "C"], ["A", "B"])
    assert correct_sequence(["A", "B", "C"], ["A", "C"])
    assert correct_sequence(["A", "B", "C"], ["B", "C"])

    # One missing token, incorrect order
    assert not correct_sequence(["A", "B", "C"], ["C", "B"])
    assert not correct_sequence(["A", "B", "C"], ["C", "A"])

    # One missing token and one extra token
    assert not correct_sequence(["A", "B"], ["A", "C"])

    # Two missing tokens
    assert correct_sequence(["A", "B", "C"], ["A"])
    assert correct_sequence(["A", "B", "C"], ["B"])
    assert correct_sequence(["A", "B", "C"], ["C"])
    assert correct_sequence(["A", "B", "C", "D"], ["A", "B"])
    assert correct_sequence(["A", "B", "C", "D"], ["A", "C"])
    assert correct_sequence(["A", "B", "C", "D"], ["A", "D"])
    assert correct_sequence(["A", "B", "C", "D"], ["B", "C"])
    assert correct_sequence(["A", "B", "C", "D"], ["B", "D"])
    assert correct_sequence(["A", "B", "C", "D"], ["C", "D"])

    # Two missing, incorrect order
    assert not correct_sequence(["A", "B", "C", "D"], ["C", "B"])

    # Two missing tokens and one extra token
    assert not correct_sequence(["A", "B", "C"], ["A", "D"])


def add_and_check(
    window: Window,
    value: typing.Any,
    expected_tokens: list,
    expected_first: int,
    expected_last: int,
):
    # Add the value to the window
    window.add_token(value)

    # Check the values
    actual_tokens, first, last = window.get_tokens()
    assert actual_tokens == expected_tokens
    assert first == expected_first
    assert last == expected_last


def test_window():
    # Window of length 1
    #
    # Index:   0  1  2
    # Value:  10 20 30
    # Window: ==
    #            ==
    #               ==
    w = Window(1)
    add_and_check(w, 10, [10], 0, 0)
    add_and_check(w, 20, [20], 1, 1)
    add_and_check(w, 30, [30], 2, 2)

    # Window of length 2
    #
    # Index:   0  1  2
    # Value:  10 20 30
    # Window: ==
    #         =====
    #            =====
    w = Window(2)
    add_and_check(w, 10, [10], 0, 0)
    add_and_check(w, 20, [10, 20], 0, 1)
    add_and_check(w, 30, [20, 30], 1, 2)

    # Window of length 3
    #
    # Index:   0  1  2  3  4
    # Value:  10 20 30 40 50
    # Window: ==
    #         =====
    #         ========
    #            ========
    #               ========
    w = Window(3)
    add_and_check(w, 10, [10], 0, 0)
    add_and_check(w, 20, [10, 20], 0, 1)
    add_and_check(w, 30, [10, 20, 30], 0, 2)
    add_and_check(w, 40, [20, 30, 40], 1, 3)
    add_and_check(w, 50, [30, 40, 50], 2, 4)
