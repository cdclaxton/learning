import random
import math
import matplotlib.pyplot as plt


def connection_lookup(num_nodes, adjacency_list):
    """Create a dict of the connections from a node to its neighbours."""
    assert num_nodes >= 0
    assert type(adjacency_list) == list

    # Initialise the lookup
    lookup = {i: [] for i in range(num_nodes)}

    # Add each edge to the lookup
    for src, dst in adjacency_list:
        lookup[src].append(dst)
        lookup[dst].append(src)

    # Sort the destinations
    lookup = {src: sorted(dst) for src, dst in lookup.items()}

    return lookup


def test_connection_lookup():
    """Unit tests for connection_lookup()."""
    assert connection_lookup(2, []) == {0: [], 1: []}
    assert connection_lookup(2, [(0, 1)]) == {0: [1], 1: [0]}
    assert connection_lookup(3, [(0, 1)]) == {0: [1], 1: [0], 2: []}
    assert connection_lookup(3, [(0, 1), (1, 2)]) == {0: [1], 1: [0, 2], 2: [1]}
    assert connection_lookup(3, [(0, 1), (1, 2), (0, 2)]) == {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1],
    }
    assert connection_lookup(4, [(0, 3), (3, 1), (0, 1), (3, 2)]) == {
        0: [1, 3],
        1: [0, 3],
        2: [3],
        3: [0, 1, 2],
    }


def calc_overlap(node_sequence, adjacency_list):
    """Calculate the number of overlapping edges."""
    assert type(node_sequence) == list
    assert len(node_sequence) > 0
    assert type(adjacency_list) == list

    # Create a connection lookup to quickly find which other nodes a given node
    # is connected to
    lookup = connection_lookup(len(node_sequence), adjacency_list)

    gaps = [0 for _ in range(len(node_sequence) - 1)]

    # Walk through each node in the sequence, except the last
    for i in range(len(node_sequence) - 1):
        # Source node
        src = node_sequence[i]

        # Walk through each of the nodes connected to the source node
        for dst in lookup[src]:
            # Is the destination node behind the source node? If so, it's
            # already been considered
            behind = node_sequence[:i]
            if dst in behind:
                continue

            for j in range(i + 1, len(node_sequence)):
                gaps[j - 1] += 1
                if node_sequence[j] == dst:
                    break

    # print(f"Node sequence: {node_sequence}, Adj: {adjacency_list}, gaps: {gaps}")
    overlap = sum([g > 1 for g in gaps])

    return overlap


def test_calc_overlap():
    """Unit tests for calc_overlap()."""

    # Disconnected nodes
    node_sequence = [0, 1]
    adjacency_list = []
    assert calc_overlap(node_sequence, adjacency_list) == 0

    # Two nodes, connected
    node_sequence = [0, 1]
    adjacency_list = [(0, 1)]
    assert calc_overlap(node_sequence, adjacency_list) == 0

    # Three nodes, no overlap
    node_sequence = [0, 1, 2]
    adjacency_list = [(0, 1), (1, 2)]
    assert calc_overlap(node_sequence, adjacency_list) == 0

    # Three nodes, overlap
    node_sequence = [0, 1, 2]
    adjacency_list = [(0, 1), (0, 2)]
    assert calc_overlap(node_sequence, adjacency_list) == 1

    # Three nodes, overlap
    node_sequence = [0, 1, 2]
    adjacency_list = [(0, 1), (0, 2), (1, 2)]
    assert calc_overlap(node_sequence, adjacency_list) == 2

    # Three nodes, no overlap
    node_sequence = [2, 0, 1]
    adjacency_list = [(2, 0), (0, 1)]
    assert calc_overlap(node_sequence, adjacency_list) == 0

    # Four nodes, overlap
    node_sequence = [0, 2, 1, 3]
    adjacency_list = [(0, 2), (0, 1), (1, 3)]
    assert calc_overlap(node_sequence, adjacency_list) == 1

    # Four nodes, overlap
    node_sequence = [0, 3, 1, 2]
    adjacency_list = [(0, 3), (3, 1), (0, 1), (3, 2)]
    assert calc_overlap(node_sequence, adjacency_list) == 2

    # Five nodes, overlap
    node_sequence = [0, 1, 3, 4, 2]
    adjacency_list = [(0, 1), (0, 3), (1, 4), (4, 2)]
    assert calc_overlap(node_sequence, adjacency_list) == 2


def randomly_switch_nodes(node_sequence):
    """Randomly switch two nodes in the sequence."""

    n2 = node_sequence[:]

    idx1, idx2 = 0, 0
    while idx1 == idx2:
        idx1 = random.randint(0, len(node_sequence) - 1)
        idx2 = random.randint(0, len(node_sequence) - 1)

    n2[idx1] = node_sequence[idx2]
    n2[idx2] = node_sequence[idx1]

    return n2


def optimise(node_sequence, adjacency_list):
    """Optimise the sequence of nodes using random switching."""

    assert type(node_sequence) == list
    assert len(node_sequence) > 0
    assert type(adjacency_list) == list

    current_overlap = calc_overlap(node_sequence, adjacency_list)

    for _ in range(100):
        potential_node_sequence = randomly_switch_nodes(node_sequence)
        potential_overlap = calc_overlap(potential_node_sequence, adjacency_list)

        if potential_overlap < current_overlap:
            print(f"Accepting {potential_node_sequence} -> {potential_overlap}")
            accept = True
        else:
            accept = False

        if accept:
            node_sequence = potential_node_sequence
            current_overlap = potential_overlap

    return node_sequence


def optimise_simulated_annealing(node_sequence, adjacency_list):
    """Optimise the sequence of nodes using simulated annealing."""

    assert type(node_sequence) == list
    assert len(node_sequence) > 0
    assert type(adjacency_list) == list

    current_overlap = calc_overlap(node_sequence, adjacency_list)

    k_max = 100
    for k in range(k_max):
        # Temperature
        T = 1 - (k + 1) / k_max

        potential_node_sequence = randomly_switch_nodes(node_sequence)
        potential_overlap = calc_overlap(potential_node_sequence, adjacency_list)

        # Calculate the acceptance probability
        if potential_overlap < current_overlap:
            prob = 1.0
        elif potential_overlap == current_overlap:
            prob = 0.0
        else:
            prob = math.exp(-(potential_overlap - current_overlap) / (T + 1e-6))

        if prob > random.random():
            print(f"SA Accepting {potential_node_sequence} -> {potential_overlap}")
            node_sequence = potential_node_sequence
            current_overlap = potential_overlap

    return node_sequence


def random_adjacency_list(num_nodes, num_edges):
    """Generate a random adjacency list."""

    assert num_nodes > 0
    assert num_edges >= 0

    edges = []
    for _ in range(num_edges):
        generated_edge = False

        while not generated_edge:
            # Generate a distinct source and destination
            idx1, idx2 = 0, 0
            while idx1 == idx2:
                idx1 = random.randint(0, num_nodes - 1)
                idx2 = random.randint(0, num_nodes - 1)

            if idx1 > idx2:
                idx1, idx2 = idx2, idx1

            pair = (idx1, idx2)
            if pair not in edges:
                edges.append(pair)
                generated_edge = True

    return edges


def plot_original_optimised(
    seq_original, seq_optimised, seq_optimised_sa, adjacency_list
):
    """Plot the original and optimised sequence of nodes."""

    assert type(seq_original) == list
    assert type(seq_optimised) == list
    assert type(seq_optimised_sa) == list
    assert len(seq_original) == len(seq_optimised)
    assert type(adjacency_list) == list

    # Calculate the overlaps
    original_overlap = calc_overlap(seq_original, adjacency_list)
    optimised_overlap = calc_overlap(seq_optimised, adjacency_list)
    sa_optimised_overlap = calc_overlap(seq_optimised_sa, adjacency_list)

    fig, axs = plt.subplots(3)
    axs[0].set_title(f"Original (overlap = {original_overlap})")
    axs[1].set_title(f"Optimised (overlap = {optimised_overlap})")
    axs[2].set_title(f"Optimised using SA (overlap = {sa_optimised_overlap})")

    # Plot the original sequence
    for src, dst in adjacency_list:
        idx0 = seq_original.index(src)
        idx1 = seq_original.index(dst)
        xs = [idx0, (idx0 + idx1) / 2, idx1]
        ys = [0, 0.5, 0]
        axs[0].plot(xs, ys)

    ticks = [float(i) for i in range(len(seq_original))]
    labels = [str(i) for i in seq_original]
    axs[0].set_xticks(ticks, labels=labels)

    # Plot the optimised sequence
    for src, dst in adjacency_list:
        idx0 = seq_optimised.index(src)
        idx1 = seq_optimised.index(dst)
        xs = [idx0, (idx0 + idx1) / 2, idx1]
        ys = [0, 0.5, 0]
        axs[1].plot(xs, ys)

    ticks = [float(i) for i in range(len(seq_optimised))]
    labels = [str(i) for i in seq_optimised]
    axs[1].set_xticks(ticks, labels=labels)

    # Plot the optimised sequence using SA
    for src, dst in adjacency_list:
        idx0 = seq_optimised_sa.index(src)
        idx1 = seq_optimised_sa.index(dst)
        xs = [idx0, (idx0 + idx1) / 2, idx1]
        ys = [0, 0.5, 0]
        axs[2].plot(xs, ys)

    ticks = [float(i) for i in range(len(seq_optimised_sa))]
    labels = [str(i) for i in seq_optimised_sa]
    axs[2].set_xticks(ticks, labels=labels)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Run tests
    test_connection_lookup()
    test_calc_overlap()

    # Show a small example
    node_sequence = [0, 1, 3, 4, 2]
    adjacency_list = [(0, 1), (0, 3), (1, 4), (4, 2)]
    optimise(node_sequence, adjacency_list)

    # Generate a random dataset
    num_nodes = 8
    num_edges = 6
    node_sequence = list(range(num_nodes))
    adjacency_list = random_adjacency_list(num_nodes, num_edges)

    # Optimise the node sequence
    node_sequence_original = node_sequence[:]
    node_sequence_optimised = optimise(node_sequence, adjacency_list)
    node_sequence_optimised_sa = optimise_simulated_annealing(
        node_sequence, adjacency_list
    )

    plot_original_optimised(
        node_sequence_original,
        node_sequence_optimised,
        node_sequence_optimised_sa,
        adjacency_list,
    )
