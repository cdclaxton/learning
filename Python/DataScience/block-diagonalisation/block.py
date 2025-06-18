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
    """Build the reordered matrix."""

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

    return reorder_matrix(ordering, matrix), ordering


def random_pair(N):
    """Generate a random pair of distinct values in the range [0, N-1]."""
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


def block_diagonalise(matrix, initial_ordering):

    n_rows, n_cols = matrix.shape
    assert n_rows == n_cols

    ordering = initial_ordering[:]
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

    # Build a random symmetric block diagonal matrix
    matrix = build_matrix()

    # Shuffle the rows and columns of the matrix
    shuffled, shuffled_ordering = shuffle_matrix(matrix)

    # Perform block diagonalisation
    block_ordering = block_diagonalise(matrix, shuffled_ordering)
    result = reorder_matrix(block_ordering, matrix)

    # Number of rows and columns in the matrix
    n = len(block_ordering)

    plt.subplot(1, 3, 1)
    plt.imshow(matrix)
    plt.xticks(np.arange(n))
    plt.yticks(np.arange(n))
    plt.title("Original")

    plt.subplot(1, 3, 2)
    plt.imshow(shuffled)
    plt.xticks(np.arange(n), shuffled_ordering)
    plt.yticks(np.arange(n), shuffled_ordering)
    plt.title("Shuffled")

    plt.subplot(1, 3, 3)
    plt.imshow(result)
    plt.xticks(np.arange(n), block_ordering)
    plt.yticks(np.arange(n), block_ordering)
    plt.title("Reordered")

    plt.show()
    # plt.savefig("example.png")
