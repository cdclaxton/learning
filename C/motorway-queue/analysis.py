import ctypes
import matplotlib.pyplot as plt
import numpy as np

# Load the DLL
lib_name = "./libmotorway.so"
motorway_lib = ctypes.CDLL(lib_name)

# Argument and return types for the C simulate() function
motorway_lib.simulate.argtypes = (
    ctypes.c_double,
    ctypes.c_int,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
)
motorway_lib.simulate.restype = ctypes.POINTER(ctypes.c_double)


def mph_to_ms(mph):
    return (mph * 1609.344) / (60 * 60)


def plot_no_blockage_times():
    """Plot journey time with no blockages."""

    distance_in_m = 16550 + 5000 + 10750

    speed_in_mph = np.arange(30, 100, 1)
    speed_in_ms = [mph_to_ms(mph) for mph in speed_in_mph]

    time_in_s = [distance_in_m / s for s in speed_in_ms]

    plt.plot(speed_in_mph, time_in_s)
    plt.xlabel("Speed (mph)")
    plt.ylabel("Time (s)")
    plt.ylim([0, max(time_in_s) + 10])
    plt.title(f"Journey time (distance = {distance_in_m} m)")
    plt.savefig("./images/times-no-blockages.png")
    plt.clf()


def calc_journey_times(
    speed_in_ms, number_of_runs, time_delta, p_blockage, blockage_duration_s
):
    raw_journey_times = motorway_lib.simulate(
        ctypes.c_double(speed_in_ms),
        ctypes.c_int(number_of_runs),
        ctypes.c_double(time_delta),
        ctypes.c_double(p_blockage),
        ctypes.c_double(blockage_duration_s),
    )

    journey_times = []
    for i in range(number_of_runs):
        journey_times.append(raw_journey_times[i])

    motorway_lib.freeResults(raw_journey_times)

    return journey_times


def plot_blockage_times():

    number_of_blockages_per_hour = [0, 1, 2, 4, 8, 16]
    speeds_in_mph = [55, 60, 65, 70, 75, 80]
    speed_in_ms = [mph_to_ms(mph) for mph in speeds_in_mph]

    number_of_runs = 10000
    time_delta = 1.0

    num_ticks_per_hour = 60 * 60 / time_delta
    blockage_duration_s = 60.0 * 10

    for n_blockages in number_of_blockages_per_hour:

        p_blockage = n_blockages / num_ticks_per_hour

        journey_times = [
            np.mean(
                calc_journey_times(
                    s, number_of_runs, time_delta, p_blockage, blockage_duration_s
                )
            )
            for s in speed_in_ms
        ]

        plt.plot(speeds_in_mph, journey_times, label=f"{n_blockages} blockages/hour")

    plt.xlabel("Speed (mph)")
    plt.ylabel("Time (s)")
    plt.title("Journey time for 10 minute blockages")
    plt.legend()
    plt.savefig("./images/time-with-10-min-blockage.png")
    plt.clf()


def plot_ratio_journey_times():

    speed_in_ms = [mph_to_ms(mph) for mph in [55, 80]]

    number_of_blockages_per_hour = np.arange(0, 31, 1)
    number_of_runs = 10000
    time_delta = 1.0

    num_ticks_per_hour = 60 * 60 / time_delta
    blockage_duration_s = 60.0 * 5

    ratios = []
    for n_blockages in number_of_blockages_per_hour:

        p_blockage = n_blockages / num_ticks_per_hour

        journey_times = [
            np.mean(
                calc_journey_times(
                    s, number_of_runs, time_delta, p_blockage, blockage_duration_s
                )
            )
            for s in speed_in_ms
        ]

        ratios.append(journey_times[0] / journey_times[1])

    plt.plot(number_of_blockages_per_hour, ratios, ".")
    plt.xlabel("Mean number of blockages per hour")
    plt.ylabel("Ratio of mean journey times")
    plt.title("Ratio of journey times at 55mph and 80 mph")
    plt.savefig("./images/ratio.png")
    plt.clf()


if __name__ == "__main__":

    plot_no_blockage_times()
    plot_blockage_times()
    plot_ratio_journey_times()
