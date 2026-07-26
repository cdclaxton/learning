# Maze solver using a backtracking algorithm

direction = "DLRU"
dr = [1, 0, 0, -1]
dc = [0, -1, 1, 0]


def is_valid(row, col, n, maze):
    return 0 <= row < n and 0 <= col < n and maze[row][col] == 1


def find_path(row, col, maze, path, solutions):
    # Length of a side of the square maze
    n = len(maze)

    # If the destination has been reached, then store the path as a solution
    if row == n - 1 and col == n - 1:
        solutions.append("".join(path))
        return

    # Mark the current cell as having been visited
    maze[row][col] = 0

    # Check each possible direction (up, down, left and right)
    for i in range(4):
        next_row, next_col = row + dr[i], col + dc[i]
        if is_valid(next_row, next_col, n, maze):
            path.append(direction[i])

            # Move to the next cell
            find_path(next_row, next_col, maze, path, solutions)

            # Backtrack
            path.pop()

    # Unmark the current cell
    maze[row][col] = 1


def solve_maze(maze):
    # Length of a side of the square maze
    n = len(maze)

    # Check that the maze is valid
    assert maze[0][0] == 1 and maze[n - 1][n - 1] == 1, (
        "Start and exit must be at (0,0) and (n-1, n-1)"
    )

    # Initialise the list that will hold the solutions
    solutions = []

    # Current path through the maze
    path = []

    # Find the paths through the maze and then sort them
    find_path(0, 0, maze, path, solutions)
    solutions.sort()

    return solutions


if __name__ == "__main__":
    # Define the square maze. A 1 means that the cell is open, 0 means blocked
    maze = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 1, 1],
    ]

    for solution in solve_maze(maze):
        print(solution)
