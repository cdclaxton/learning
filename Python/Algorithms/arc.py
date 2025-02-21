import matplotlib.pyplot as plt
import numpy as np


def degrees_to_radians(d):
    # 180 degrees = pi radians
    # therefore, 1 degree = pi / 180 radians
    return d * np.pi / 180


def radians_to_degrees(r):
    return r * 180 / np.pi


def rotate_points(X, theta):
    """Rotate the points in X by theta radians."""
    assert X.shape[0] == 2
    assert type(theta) == float

    # Rotation matrix
    rotation_matrix = np.array(
        [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)],
        ]
    )

    # M = 2x2, X = 2xN, M * X = 2xN
    return np.matmul(rotation_matrix, X)


def translate_points(X, delta):
    assert X.shape[0] == 2
    assert delta.shape == (2, 1)

    return X + delta


def points_on_circle_clockwise(n_points, turn_angle_radians, radius):
    assert type(n_points) == int and n_points > 2
    assert type(turn_angle_radians) == float
    assert type(radius) == float and radius > 0

    thetas = np.linspace(
        degrees_to_radians(90), degrees_to_radians(90) - turn_angle_radians, n_points
    )

    # 2xN matrix of points on a circle
    P = np.zeros((2, n_points))

    for i, theta in enumerate(thetas):
        P[0, i] = radius * np.cos(theta)
        P[1, i] = radius * (-1 + np.sin(theta))

    return P


def points_on_circle_anticlockwise(n_points, turn_angle_radians, radius):
    assert type(n_points) == int and n_points > 2
    assert type(turn_angle_radians) == float
    assert type(radius) == float and radius > 0

    thetas = np.linspace(
        degrees_to_radians(90), degrees_to_radians(90) - turn_angle_radians, n_points
    )

    # 2xN matrix of points on a circle
    P = np.zeros((2, n_points))

    for i, theta in enumerate(thetas):
        P[0, i] = radius * np.cos(theta)
        P[1, i] = radius * (1 - np.sin(theta))

    return P


def arc(
    start_x, start_y, enter_angle_degrees, turn_degrees, clockwise, n_points, radius
):

    # Start position
    start = np.array([[start_x, start_y]]).transpose()

    # End angle
    turn_angle_radians = degrees_to_radians(turn_degrees)

    # Generate the points (2 * n_points)
    if clockwise:
        P = points_on_circle_clockwise(n_points, turn_angle_radians, radius)
    else:
        P = points_on_circle_anticlockwise(n_points, turn_angle_radians, radius)

    # Rotate
    P1 = rotate_points(P, degrees_to_radians(enter_angle_degrees))

    # Translate
    P2 = translate_points(P1, start)

    return P2


if __name__ == "__main__":

    start_x = 3
    start_y = 2
    enter_angle_degrees = 45

    P = arc(
        start_x=start_x,
        start_y=start_y,
        enter_angle_degrees=enter_angle_degrees,
        turn_degrees=120,
        clockwise=False,
        n_points=10,
        radius=3.0,
    )

    plt.plot(P[0, :], P[1, :], "or")

    # First point
    plt.plot([start_x], [start_y], "go")

    # Second point
    plt.plot(P[0, 1], P[1, 1], "bo")

    # Plot a line to denote the turn enter angle
    d = 2
    plt.plot(
        [start_x - d * np.cos(degrees_to_radians(enter_angle_degrees)), start_x],
        [start_y - d * np.sin(degrees_to_radians(enter_angle_degrees)), start_y],
        "-k",
    )

    plt.axis("square")
    plt.xlim(-8, 8)
    plt.ylim(-8, 8)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
