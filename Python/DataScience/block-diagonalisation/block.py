import numpy as np
import matplotlib.pyplot as plt
import random


def build_matrix():
    """Build a block diagonal matrix."""

    structure = np.array(
        [
            [1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1],
        ]
    )

    n_rows = structure.shape[0]
    for i in range(n_rows):
        for j in range(i, n_rows):
            if structure[i, j] == 1:
                structure[i, j] = np.random.randint(50, 100)
            else:
                structure[i, j] = np.random.randint(1, 20)

            structure[j, i] = structure[i, j]

    return structure


def reorder_matrix(ordering, matrix):

    n_rows = matrix.shape[0]

    result = np.zeros((n_rows, n_rows))
    for i, new_i in enumerate(ordering):
        for j, new_j in enumerate(ordering):
            result[i, j] = matrix[new_i, new_j]

    return result


def shuffle_matrix(matrix):
    """Shuffle the rows and columns of the matrix."""

    n_rows, n_cols = matrix.shape
    assert n_rows == n_cols

    ordering = list(range(n_rows))
    random.shuffle(ordering)

    return reorder_matrix(ordering, matrix)


def random_pair(N):
    x1 = np.random.randint(N)
    x2 = np.random.randint(N)
    while x1 == x2:
        x2 = np.random.randint(N)

    return x1, x2


def calc_distance(matrix, ordering):

    n_rows = matrix.shape[0]
    distance = 0

    result = reorder_matrix(ordering, matrix)
    for i in range(n_rows):
        for j in range(n_rows):
            distance += abs(i - j) * result[i, j]

    return distance


def block_diagonalise(matrix):

    n_rows, n_cols = matrix.shape
    assert n_rows == n_cols

    ordering = list(range(n_rows))
    initial_distance = calc_distance(matrix, ordering)

    for _ in range(50):
        candidate_ordering = ordering[:]
        x1, x2 = random_pair(n_rows)
        candidate_ordering[x1], candidate_ordering[x2] = (
            candidate_ordering[x2],
            candidate_ordering[x1],
        )

        new_distance = calc_distance(matrix, candidate_ordering)

        if new_distance < initial_distance:
            initial_distance = new_distance
            ordering = candidate_ordering

    return ordering


if __name__ == "__main__":

    matrix = build_matrix()

    shuffled = shuffle_matrix(matrix)

    block_ordering = block_diagonalise(shuffled)
    result = reorder_matrix(block_ordering, shuffled)

    plt.subplot(1, 2, 1)
    plt.imshow(shuffled)
    plt.title("Shuffled")

    plt.subplot(1, 2, 2)
    plt.imshow(result)
    plt.xticks(np.arange(len(block_ordering)), block_ordering)
    plt.yticks(np.arange(len(block_ordering)), block_ordering)
    plt.title("Reordered")

    plt.show()
