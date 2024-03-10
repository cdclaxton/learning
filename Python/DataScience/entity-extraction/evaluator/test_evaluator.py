from .evaluator import *


def test_entity_span():
    e1 = EntitySpan(1, 1, 100)
    assert len(e1) == 1

    e1 = EntitySpan(1, 2, 100)
    assert len(e1) == 2

    e1 = EntitySpan(10, 14, 100)
    assert len(e1) == 5


def test_pad():
    x = [1, 2, 3]
    assert pad(x, 3) == [1, 2, 3]
    assert pad(x, 4) == [1, 2, 3, None]
    assert pad(x, 5) == [1, 2, 3, None, None]


def test_pairs():
    # One element
    x = [1]
    y = [5]
    assert pairs(x, y) == [[(1, 5)]]

    # Two elements
    x = [1, 2]
    y = [5, 6]
    assert pairs(x, y) == [[(1, 5), (2, 6)], [(1, 6), (2, 5)]]

    # Three elements
    x = [1, 2, 3]
    y = [5, 6, 7]
    assert pairs(x, y) == [
        [(1, 5), (2, 6), (3, 7)],
        [(1, 5), (2, 7), (3, 6)],
        [(1, 6), (2, 5), (3, 7)],
        [(1, 6), (2, 7), (3, 5)],
        [(1, 7), (2, 5), (3, 6)],
        [(1, 7), (2, 6), (3, 5)],
    ]


def test_error_pair():
    e1 = EntitySpan(0, 0, 100)  # Span of 1
    e2 = EntitySpan(0, 1, 101)  # Span of 2

    # None and None
    assert error_pair(None, None) == 0

    # None and entity span of 1
    assert error_pair(None, e1) == 1
    assert error_pair(e1, None) == 1

    # None and entity span of 2
    assert error_pair(None, e2) == 2
    assert error_pair(e2, None) == 2

    # No overlap, non-adjacent
    # Index       0 1 2 3 4 5 6 7 8 9 10
    # Entity 1      1 1 1
    # Entity 2              1 1
    # Errors        * * *   * *
    entity1 = EntitySpan(1, 3, 1)
    entity2 = EntitySpan(5, 6, 1)
    assert error_pair(entity1, entity2) == 5

    # No overlap, adjacent
    # Index       0 1 2 3 4 5 6 7 8 9 10
    # Entity 1      1 1 1
    # Entity 2            1 1 1
    # Errors        * * * * * *
    entity1 = EntitySpan(1, 3, 1)
    entity2 = EntitySpan(4, 6, 1)
    assert error_pair(entity1, entity2) == 6

    # Overlap, different entity
    # Index       0 1 2 3 4 5 6 7 8 9 10
    # Entity 1      1 1 1
    # Entity 2      2 2
    # Errors        * * *
    entity1 = EntitySpan(1, 3, 1)
    entity2 = EntitySpan(1, 2, 2)
    assert error_pair(entity1, entity2) == 3

    # Complete overlap, same entity
    # Index       0 1 2 3 4 5 6 7 8 9 10
    # Entity 1      1 1 1
    # Entity 2      1 1 1
    # Errors
    entity1 = EntitySpan(1, 3, 1)
    entity2 = EntitySpan(1, 3, 1)
    assert error_pair(entity1, entity2) == 0

    # Partial overlap, same entity
    # Index       0 1 2 3 4 5 6 7 8 9 10
    # Entity 1      1 1 1
    # Entity 2      1 1
    # Errors            *
    entity1 = EntitySpan(1, 3, 1)
    entity2 = EntitySpan(1, 2, 1)
    assert error_pair(entity1, entity2) == 1

    # Partial overlap, same entity
    # Index       0 1 2 3 4 5 6 7 8 9 10
    # Entity 1          1 1 1 1 1 1
    # Entity 2              1 1 1
    # Errors            * *       *
    entity1 = EntitySpan(3, 8, 1)
    entity2 = EntitySpan(5, 7, 1)
    assert error_pair(entity1, entity2) == 3


def test_calc_error():
    # Complete overlap
    # One ground truth entity, one actual entity
    # Index         0 1 2 3 4 5 6 7 8 9 10 11 12
    # Ground truth    1 1 1
    # Actual          1 1 1
    # Errors
    ground_truth = [EntitySpan(1, 3, 1)]
    actual = [EntitySpan(1, 3, 1)]
    assert calc_error(ground_truth, actual) == 0

    # Complete overlap, different entities
    # One ground truth entity, one actual entity
    # Index         0 1 2 3 4 5 6 7 8 9 10 11 12
    # Ground truth    1 1 1
    # Actual          2 2 2
    # Errors          * * *
    ground_truth = [EntitySpan(1, 3, 1)]
    actual = [EntitySpan(1, 3, 2)]
    assert calc_error(ground_truth, actual) == 3

    # Partial overlap, same entity
    # One ground truth entity, one actual entity
    # Index         0 1 2 3 4 5 6 7 8 9 10 11 12
    # Ground truth    1 1 1
    # Actual            1 1 1
    # Errors          *     *
    ground_truth = [EntitySpan(1, 3, 1)]
    actual = [EntitySpan(2, 4, 1)]
    assert calc_error(ground_truth, actual) == 2

    # Two ground truth entities, one actual entity
    #
    # Index         0 1 2 3 4 5 6 7 8 9 10 11 12
    # Ground truth    1 1 1     2 2 2
    # Actual          1 1 1
    # Errors                    * * *
    ground_truth = [EntitySpan(1, 3, 1), EntitySpan(6, 8, 2)]
    actual = [EntitySpan(1, 3, 1)]
    assert calc_error(ground_truth, actual) == 3

    # Two ground truth entities, one actual entity
    # Partial overlap
    # Index         0 1 2 3 4 5 6 7 8 9 10 11 12
    # Ground truth    1 1 1     2 2 2
    # Actual            1 1 1
    # Errors          *     *   * * *
    ground_truth = [EntitySpan(1, 3, 1), EntitySpan(6, 8, 2)]
    actual = [EntitySpan(2, 4, 1)]
    assert calc_error(ground_truth, actual) == 5

    # Two ground truth entities, two actual entities
    #
    # Index         0 1 2 3 4 5 6 7 8 9 10 11 12
    # Ground truth    1 1 1     2 2 2
    # Actual            1 1 1   2 2
    # Errors          *     *       *
    ground_truth = [EntitySpan(1, 3, 1), EntitySpan(6, 8, 2)]
    actual = [EntitySpan(2, 4, 1), EntitySpan(6, 7, 2)]
    assert calc_error(ground_truth, actual) == 3

    # Three ground truth entities, two actual entities
    #
    # Index         0 1 2 3 4 5 6 7 8 9 10 11 12
    # Ground truth    1 1 1     2 2 2   3  3
    # Actual            1 1 1   2 2
    # Errors          *     *       *   *  *
    ground_truth = [
        EntitySpan(1, 3, 1),
        EntitySpan(6, 8, 2),
        EntitySpan(10, 11, 3),
    ]
    actual = [EntitySpan(2, 4, 1), EntitySpan(6, 7, 2)]
    assert calc_error(ground_truth, actual) == 5
