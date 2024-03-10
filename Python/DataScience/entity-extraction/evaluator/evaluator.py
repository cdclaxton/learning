# Entity extraction performance evaluator
import itertools

from domain import assert_entity_id_valid


class EntitySpan:
    def __init__(self, start: int, end: int, entity_id: int):
        assert type(start) == int
        assert type(end) == int
        assert end >= start
        assert_entity_id_valid(entity_id)

        self.start = start  # Start index
        self.end = end  # Stop index (inclusive)
        self.entity_id = entity_id  # Entity ID

    def __len__(self):
        return self.end - self.start + 1

    def in_span(self, i):
        return self.start <= i and i <= self.end

    def __repr__(self):
        return f"EntitySpan({self.start}, {self.end}, {self.entity_id})"

    def __str__(self):
        return self.__repr__()


def error_pair(s1, s2):
    """Error between the two entity spans."""

    assert s1 is None or type(s1) == EntitySpan
    assert s2 is None or type(s2) == EntitySpan

    if s1 is None and s2 is None:
        return 0
    elif s1 is None and s2 is not None:
        return len(s2)
    elif s1 is not None and s2 is None:
        return len(s1)

    min_x = min(s1.start, s2.start)
    max_x = max(s1.end, s2.end)

    same_entity = s1.entity_id == s2.entity_id
    total = 0
    for i in range(min_x, max_x + 1):
        s1_present = s1.in_span(i)
        s2_present = s2.in_span(i)

        if not (
            (not s1_present and not s2_present)
            or (s1_present and s2_present and same_entity)
        ):
            total += 1

    return total


def pad(spans, number):
    """Pad the entity spans to the required length."""

    assert type(spans) == list
    assert type(number) == int and number > 0
    assert number >= len(spans)

    N = number - len(spans)
    spans.extend([None for _ in range(N)])

    return spans


def pairs(x, y):
    """Generate all pairs of elements of x and y."""
    assert len(x) == len(y)

    N = len(x)
    all_pairs = []

    for seq in itertools.permutations(y):
        all_pairs.append([(x[i], seq[i]) for i in range(N)])

    return all_pairs


def calc_error(ground_truth, actual):
    """Calculate the error between the actual and the ground-truth entities."""

    assert type(ground_truth) == list
    assert all([type(g) == EntitySpan for g in ground_truth])
    assert type(actual) == list
    assert all([type(a) == EntitySpan for a in actual])

    max_number = max(len(ground_truth), len(actual))
    if max_number == 0:
        return 0

    # Pad the lists
    ground_truth = pad(ground_truth, max_number)
    actual = pad(actual, max_number)

    # Calculate the error for all possible pairings
    errors = []
    for seq in pairs(ground_truth, actual):
        total = 0
        for pair in seq:
            total += error_pair(pair[0], pair[1])

        errors.append(total)

    # Return the minimum error
    return min(errors)
