import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from dataclasses import dataclass
from scipy import stats


@dataclass
class Task:
    time_index: int  # Time at which the task takes place


@dataclass
class CallTask(Task):
    caller: int
    callee: int


@dataclass
class MoveTask(Task):
    phone_index: int
    location_to_move_to: int

class Schedule:
    def __init__(self, time_step_minutes: int, home_location: int):
        assert time_step_minutes > 0
        self._time_step_minutes = time_step_minutes

        self._schedule = []

    def add(self, )
        
    


def continuous_uniform(min_value, max_value):
    dist = stats.uniform(min_value, max_value - min_value)

    def f():
        return dist.rvs()

    return f


def build_directed_weighted_graph(
    undirected_graph,
    p_reciprocal_calls,
    mean_num_calls_per_day_generator,
    time_step_in_mins,
):
    assert time_step_in_mins > 0

    num_time_steps_per_day = 60 * 24 / time_step_in_mins

    directed_weighted_graph = []

    for edge in undirected_graph.edges():

        set_edge_01, set_edge_10 = True, True

        # Are calls reciprocated?
        if stats.bernoulli.rvs(p_reciprocal_calls) == 0:
            if stats.bernoulli.rvs(0.5) == 1:
                set_edge_10 = False
            else:
                set_edge_01 = False

        if set_edge_01:
            directed_weighted_graph.append(
                (
                    edge[0],
                    edge[1],
                    mean_num_calls_per_day_generator() / num_time_steps_per_day,
                )
            )

        if set_edge_10:
            directed_weighted_graph.append(
                (
                    edge[1],
                    edge[0],
                    mean_num_calls_per_day_generator() / num_time_steps_per_day,
                )
            )

    return directed_weighted_graph


def num_calls_per_day(mu):
    """Plot a histogram of the number of calls on a given day."""

    time_step_in_mins = 10
    n_timesteps_per_day = int(60 * 24 / time_step_in_mins)

    def simulate_num_calls_in_day(p_call_in_time_step):
        return np.sum(
            stats.bernoulli.rvs(p_call_in_time_step, size=n_timesteps_per_day)
        )

    mu_for_timestep = mu / n_timesteps_per_day
    n_calls = [simulate_num_calls_in_day(mu_for_timestep) for _ in range(100)]

    plt.hist(n_calls)
    plt.xlabel("Number of calls on a given day")
    plt.ylabel("Frequency")
    plt.show()


def p_locations(n_locations):
    """Probability of a phone being at a location."""
    p = stats.uniform.rvs(0, 1, size=n_locations)
    return p / np.sum(p)


if __name__ == "__main__":

    plot_graph = False

    n_phones = 5
    p_reciprocal_calls = 0.9
    time_step_minutes = 10
    n_locations = 20

    # num_calls_per_day(1)

    # Generate a random undirected network
    undirected_graph = nx.barabasi_albert_graph(n_phones, 1)
    if plot_graph:
        nx.draw(undirected_graph, with_labels=True)
        plt.show()

    # Build a directed network with edge weights
    mean_num_calls_per_day_generator = continuous_uniform(1 / 30, 2)
    directed_weighted_graph = build_directed_weighted_graph(
        undirected_graph,
        p_reciprocal_calls,
        mean_num_calls_per_day_generator,
        time_step_minutes,
    )

    # Define a movement schedule for each phone
    prob_location = p_locations(n_locations)
    schedule = []
    for _ in range(n_phones):


    # Phone location
    current_phone_location: list[int] = []

    # Run the simulator
    n_steps = 1 * int(60 * 24 / time_step_minutes)
    calls = []

    tasks_to_run: dict[int, list[Task]] = {}

    for time_index in range(n_steps):

        # Determine whether a call is made for a given edge in the directed
        # graph
        for src, dst, p_call in directed_weighted_graph:
            if stats.bernoulli.rvs(p_call) == 1:
                if time_index not in tasks_to_run:
                    tasks_to_run[time_index] = []

                tasks_to_run[time_index].append(CallTask(time_index, src, dst))

        # Determine if the phone should move locations

        # If there are no tasks to run, move onto the next time step
        if time_index not in tasks_to_run:
            continue

        # Deconflict the tasks for the current time step
        deconflicted_task_queue: list[Task] = []
        in_call = set()
        is_moving = set()
        for task in tasks_to_run[time_index]:
            if (
                type(task) == CallTask
                and task.caller not in in_call
                and task.callee not in in_call
            ):
                deconflicted_task_queue.append(task)
                in_call.add(task.caller)
                in_call.add(task.callee)

            elif type(task) == MoveTask and task.phone_index not in is_moving:
                deconflicted_task_queue.append(task)
                is_moving.add(task.phone_index)

        # All valid tasks for the current time step are now on the deconflicted
        # task queue
        if time_index in tasks_to_run:
            del tasks_to_run[time_index]

        # Run the tasks for the current time step
        for task in deconflicted_task_queue:
            if type(task) == CallTask:
                calls.append((time_index, task.caller, task.callee))
            elif type(task) == MoveTask:
                current_phone_location[task.phone_index] = task.location_to_move_to

    print(calls)
    print(len(tasks_to_run))
