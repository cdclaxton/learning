# Position discontinuity in 2D
from distributions import *
import math
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

# Row indices in the matrix for a track
X_POS_INDEX = 0
Y_POS_INDEX = 1
HEADING_INDEX = 2
SPEED_INDEX = 3
TIME_INDEX = 4


def l2_norm(x0, x1):
    assert len(x0) == 2
    assert len(x1) == 2

    x_delta = x1 - x0
    return np.sqrt(np.power(x_delta[0], 2) + np.power(x_delta[1], 2))


def position(track, idx):
    """Position of the platform at time index idx."""

    return track[X_POS_INDEX : (Y_POS_INDEX + 1), idx]


def platform_speed(p0, p1, time_delta):
    """Speed of the platform between two points."""

    assert len(p0) == 2, f"Got: {p0}"
    assert len(p1) == 2, f"Got: {p1}"
    assert time_delta > 0, f"Got: {time_delta}"

    distance = l2_norm(p1, p0)
    return distance / time_delta


def platform_speeds(track):
    """Speed of the platform between points."""

    # Number of track points
    n = track.shape[1]

    speeds = np.zeros(n)
    for i in range(1, n):
        speeds[i] = platform_speed(
            position(track, i),
            position(track, i - 1),
            track[TIME_INDEX, i] - track[TIME_INDEX, i - 1],
        )

    return speeds


def algorithm1(track, max_speed):
    """Offset points to remove a point where the speed is too high."""

    # Number of track points
    n = track.shape[1]

    speeds = platform_speeds(track)

    # Find the maximum speed
    idx = np.argmax(speeds)

    # If the speed doesn't exceed the maximum speed, then just return the track
    if speeds[idx] < max_speed:
        return track

    x_offset = track[X_POS_INDEX, idx]
    y_offset = track[Y_POS_INDEX, idx]

    offset = np.zeros((5, n))
    offset[X_POS_INDEX, idx:n] = -x_offset
    offset[Y_POS_INDEX, idx:n] = -y_offset
    return track + offset


def algorithm2(track, max_speed):

    # Number of track points
    n = track.shape[1]

    speeds = platform_speeds(track)

    # Find the maximum speed
    idx = np.argmax(speeds)

    # If the speed doesn't exceed the maximum speed, then just return the track
    if speeds[idx] < max_speed:
        return track

    if idx < 2:
        return algorithm1(track, max_speed)

    x_delta = track[X_POS_INDEX, idx - 1] - track[X_POS_INDEX, idx - 2]
    y_delta = track[Y_POS_INDEX, idx - 1] - track[Y_POS_INDEX, idx - 2]
    theta = np.arctan2(y_delta, x_delta)

    t_delta = track[TIME_INDEX, idx] - track[TIME_INDEX, idx - 1]
    d = (max_speed / 2) * t_delta
    x_pred = d * np.cos(theta)
    y_pred = d * np.sin(theta)

    x_offset = -track[X_POS_INDEX, idx] + x_pred
    y_offset = -track[Y_POS_INDEX, idx] + y_pred

    offset = np.zeros((5, n))
    offset[X_POS_INDEX, idx:n] = x_offset
    offset[Y_POS_INDEX, idx:n] = y_offset

    return track + offset


def final_distance_error(track, expected_position):
    assert len(expected_position) == 2

    actual_position = position(track, -1)
    return l2_norm(actual_position, expected_position)


if __name__ == "__main__":

    # --------------------------------------------------------------------------
    # Simulation parameters
    # --------------------------------------------------------------------------

    # Distribution over the number of points in a track
    n_points = discrete_uniform(5, 20)

    # Time between position samples in the track in seconds
    t_samples = 1

    # Distribution over the initial angle of the platform
    initial_theta = continuous_uniform(-math.pi, math.pi)

    # Distribution over the change in angle
    delta_theta = vonmises(0, 1)

    # Distribution over the speed of the platform in m/s
    speed = continuous_uniform(0, 10)

    # Distribution over the discontinuity distance in x and y
    discontinuity_delta = continuous_uniform(0, 100)

    # --------------------------------------------------------------------------
    # Run the simulation
    # --------------------------------------------------------------------------

    # Generate a track without a discontinuity
    n = n_points()

    track = np.zeros((5, n))
    track[HEADING_INDEX, 0] = initial_theta()

    for i in range(1, n):
        # Set the time
        track[TIME_INDEX, i] = i

        # Set the new speed and heading
        track[HEADING_INDEX, i] = track[HEADING_INDEX, i - 1] + delta_theta()
        track[SPEED_INDEX, i] = speed()

        # Distance travelled by the platform between samples
        d = track[SPEED_INDEX, i] * t_samples

        track[X_POS_INDEX, i] = track[X_POS_INDEX, i - 1] + d * np.sin(
            track[HEADING_INDEX, i]
        )
        track[Y_POS_INDEX, i] = track[Y_POS_INDEX, i - 1] + d * np.cos(
            track[HEADING_INDEX, i]
        )

    # Add a discontinuity to the track
    correction_index = discrete_uniform(0, n - 1)()
    print(f"Discontinuity at index {correction_index} of {n}")
    discontinuity = np.zeros((5, n))
    discontinuity[X_POS_INDEX, correction_index:n] = discontinuity_delta()
    discontinuity[Y_POS_INDEX, correction_index:n] = discontinuity_delta()

    track_with_discontinuity = track + discontinuity

    # Run algorithms to try to correct the track with a potential discontinuity
    corrected_track_1 = algorithm1(track_with_discontinuity, 10)
    corrected_track_2 = algorithm2(track_with_discontinuity, 10)

    # Error measures
    expected_position = position(track, -1)
    print(f"Error in uncorrected track: {final_distance_error(track_with_discontinuity, expected_position)}")
    print(f"Error in algorithm 1: {final_distance_error(corrected_track_1, expected_position)}")
    print(f"Error in algorithm 2: {final_distance_error(corrected_track_2, expected_position)}")

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(5, 5)

    x_pos = np.hstack(
        [
            track[X_POS_INDEX, :],
            track_with_discontinuity[X_POS_INDEX, :],
            corrected_track_1[X_POS_INDEX, :],
            corrected_track_2[X_POS_INDEX, :],
        ]
    )

    y_pos = np.hstack(
        [
            track[Y_POS_INDEX, :],
            track_with_discontinuity[Y_POS_INDEX, :],
            corrected_track_1[Y_POS_INDEX, :],
            corrected_track_2[Y_POS_INDEX, :],
        ]
    )

    x_min = np.min(x_pos) - 5
    x_max = np.max(x_pos) + 5
    y_min = np.min(y_pos) - 5
    y_max = np.max(y_pos) + 5

    def animate(i):
        ax.clear()

        # Ground truth track
        plt.plot(
            track[0, 0 : (i + 1)],
            track[1, 0 : (i + 1)],
            "-x",
            color="k",
            alpha=0.5,
            label="Ground truth",
        )

        plt.plot(
            track_with_discontinuity[0, 0 : (i + 1)],
            track_with_discontinuity[1, 0 : (i + 1)],
            "-.o",
            color="r",
            alpha=0.5,
            label="Track with discontinuity",
        )
        plt.plot(
            corrected_track_1[0, 0 : (i + 1)],
            corrected_track_1[1, 0 : (i + 1)],
            "--s",
            color="g",
            alpha=0.5,
            label="Algorithm 1",
        )
        plt.plot(
            corrected_track_2[0, 0 : (i + 1)],
            corrected_track_2[1, 0 : (i + 1)],
            "--d",
            color="b",
            alpha=0.5,
            label="Algorithm 2",
        )

        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()

    ani = FuncAnimation(fig, animate, frames=n, interval=500, repeat=True)
    plt.show()
