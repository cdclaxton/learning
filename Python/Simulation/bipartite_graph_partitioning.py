import math
from distributions import *
from graph import *


def generate_graph(
    n_chains,
    n_stores,
    primary_store_chain_weight,
    secondary_store_chain_edge,
    secondary_store_chain_weight,
    store_store_edge,
    store_store_weight,
    chain_chain_edge,
    chain_chain_weight,
):
    graph = Graph(allowed_connection_types)

    # Build the chains
    for chain_index in range(n_chains()):
        graph.add_node(f"C {chain_index}", NODE_CHAIN)

    # Build the stores
    for store_index in range(n_stores()):
        graph.add_node(f"S {store_index}", NODE_STORE)

    # Add the primary store--chain edges
    connect_nodes(graph, NODE_STORE, NODE_CHAIN)

    # Add the weights for the primary connections
    for src, dst in graph.edges_of_type(NODE_STORE, NODE_CHAIN):
        graph.set_edge_weight(src, dst, primary_store_chain_weight())

    # Add secondary store--chain edges
    for store in graph.nodes_of_type(NODE_STORE):
        for chain in graph.nodes_of_type(NODE_CHAIN):

            if graph.has_edge(store, chain) or secondary_store_chain_edge() == 0:
                continue

            graph.add_edge(store, chain)
            graph.set_edge_weight(store, chain, secondary_store_chain_weight())

    # Add store--store edges
    store_nodes = graph.nodes_of_type(NODE_STORE)
    for i in range(len(store_nodes) - 1):
        for j in range(i + 1, len(store_nodes)):

            if store_store_edge() == 1:
                graph.add_edge(store_nodes[i], store_nodes[j])
                graph.set_edge_weight(
                    store_nodes[i], store_nodes[j], store_store_weight()
                )

    # Add chain-chain edges
    chain_nodes = graph.nodes_of_type(NODE_CHAIN)
    for i in range(len(chain_nodes) - 1):
        for j in range(i + 1, len(chain_nodes)):

            if chain_chain_edge() == 1:
                graph.add_edge(chain_nodes[i], chain_nodes[j])
                graph.set_edge_weight(
                    chain_nodes[i], chain_nodes[j], chain_chain_weight()
                )

    return graph


class Partition:
    def __init__(self, root, edges=None):
        self._root = root

        if edges is None:
            self._edges: list[tuple[int, int]] = []
        else:
            self._edges = edges

    def node_in_partition(self, node: int) -> bool:
        if node == self._root:
            return True

        for src, dst in self._edges:
            if src == node or dst == node:
                return True

        return False

    def can_accept(self, edge: tuple[int, int]) -> bool:
        source, destination = edge
        return self.node_in_partition(source) or self.node_in_partition(destination)

    def add_edge(self, edge: tuple[int, int]):
        self._edges.append(edge)

    def has_edge(self, edge: tuple[int, int]) -> bool:
        return edge in self._edges

    def remove_edge(self, edge: tuple[int, int]):
        assert edge in self._edges
        self._edges.remove(edge)

    def connected_without(self, edge: tuple[int, int]):
        """Would the partition's graph be connected without the edge?"""

        if len(self._edges) == 1 and self._edges[0] == edge:
            return False

        g = nx.Graph()
        for e in self._edges:
            if e != edge:
                g.add_edge(e[0], e[1])

        return nx.is_connected(g)

    def clone(self):
        return Partition(self._root, self._edges[:])

    def nodes(self):
        return set([e[0] for e in self._edges]).union(set([e[1] for e in self._edges]))

    def __str__(self):
        return f"Partition(edges={self._edges})"

    def n_nodes(self) -> int:
        return len(self.nodes())

    def sum_edge_weight(self, graph) -> int:
        return sum([graph.edge_weight(e[0], e[1]) for e in self._edges])

    def diameter(self):
        g = nx.Graph()
        for src, dst in self._edges:
            g.add_edge(src, dst)

        try:
            return nx.diameter(g)
        except nx.exception.NetworkXPointlessConcept:
            return 0

    def __repr__(self):
        return self.__str__()


def partitions_consistent(partitions: list[Partition]) -> bool:

    edges: set[tuple[int, int]] = set()

    for p in partitions:
        for edge in p._edges:
            if edge in edges:
                return False
            edges.add(edge)

    # Check each partition is populated
    for p in partitions:
        if len(p._edges) == 0:
            return False

    return True


def initial_partition(roots, edges):

    assert no_duplicate_edges(edges)

    partitions = [Partition(node) for node in roots]
    partition_indices = list(range(len(partitions)))

    edge_used = [False for _ in range(len(edges))]

    while not all(edge_used):
        for i, edge in enumerate(edges):
            if edge_used[i]:
                continue

            random.shuffle(partition_indices)

            for p in partition_indices:
                if partitions[p].can_accept(edge):
                    edge_used[i] = True
                    partitions[p].add_edge(edge)
                    break

    assert partitions_consistent(partitions)

    return partitions


def cost(graph, partitions: list[Partition], alpha: float, beta: float) -> float:
    total = 0.0

    for partition in partitions:
        total += (
            1.0 * partition.n_nodes()
            + alpha * partition.diameter()
            + beta * (1 / partition.sum_edge_weight(graph))
        )

    return total


def no_duplicate_edges(edges: list[tuple[int, int]]) -> bool:

    processed_edges = set()
    for e in edges:
        if e in processed_edges:
            return False
        processed_edges.add(e)

    return True


def candidate_edge(partitions: list[Partition]):

    # Check the partitions are consistent
    assert partitions_consistent(partitions)

    edge: tuple[int, int] | None = None
    donor_partition_idx = -1
    acceptor_partition_idx = -1

    while edge is None:
        donor_partition_idx = random.randint(0, len(partitions) - 1)
        random_edge = random.choice(partitions[donor_partition_idx]._edges)

        # If the edge would break the partition's graph into two, it cannot
        # be a potential
        if not partitions[donor_partition_idx].connected_without(random_edge):
            continue

        other_partitions_idx = [
            i for i in range(len(partitions)) if i != donor_partition_idx
        ]
        random.shuffle(other_partitions_idx)

        for p in other_partitions_idx:
            if partitions[p].can_accept(random_edge):
                edge = random_edge
                acceptor_partition_idx = p
                break

    assert partitions[donor_partition_idx].has_edge(edge)
    assert not partitions[acceptor_partition_idx].has_edge(edge)

    return edge, donor_partition_idx, acceptor_partition_idx


def mutate_partitions(partitions, edge, donor_partition_idx, acceptor_partition_idx):
    mutated_partitions = [p.clone() for p in partitions]
    mutated_partitions[donor_partition_idx].remove_edge(edge)
    mutated_partitions[acceptor_partition_idx].add_edge(edge)

    assert partitions_consistent(partitions)

    return mutated_partitions


def local_optimisation(graph, partitions, alpha, beta):

    costs = []

    for i in range(10):

        edge, donor_partition_idx, acceptor_partition_idx = candidate_edge(partitions)

        # Cost without the swap
        cost_without_swap = cost(graph, partitions, alpha, beta)

        # Cost with the swap
        mutated_partitions = mutate_partitions(
            partitions, edge, donor_partition_idx, acceptor_partition_idx
        )
        cost_with_swap = cost(graph, mutated_partitions, alpha, beta)

        # Decide
        if cost_with_swap < cost_without_swap:
            partitions = mutated_partitions
            costs.append(cost_with_swap)
        else:
            costs.append(cost_without_swap)

    return partitions, costs


def simulated_annealing(graph, partitions, alpha, beta, T, r):

    while T > 0.01:

        edge, donor_partition_idx, acceptor_partition_idx = candidate_edge(partitions)

        # Cost without the swap
        cost_without_swap = cost(graph, partitions, alpha, beta)

        # Cost with the swap
        mutated_partitions = mutate_partitions(
            partitions, edge, donor_partition_idx, acceptor_partition_idx
        )
        cost_with_swap = cost(graph, mutated_partitions, alpha, beta)

        delta = cost_with_swap - cost_without_swap

        if cost_with_swap < cost_without_swap:
            partitions = mutated_partitions
            costs.append(cost_with_swap)

        elif random.random() < math.exp(-delta / T):
            partitions = mutated_partitions
            costs.append(cost_with_swap)

        else:
            costs.append(cost_without_swap)

        T = r * T

    return partitions, costs


if __name__ == "__main__":

    # Parameters
    n_chains = discrete_uniform(2, 3)
    n_stores = discrete_uniform(4, 8)

    primary_store_chain_weight = discrete_uniform(4, 10)

    secondary_store_chain_edge = bernoulli(0.1)
    secondary_store_chain_weight = discrete_uniform(1, 3)

    store_store_edge = bernoulli(0.1)
    store_store_weight = discrete_uniform(10, 20)

    chain_chain_edge = bernoulli(0.1)
    chain_chain_weight = discrete_uniform(100, 200)

    # Generate a random graph
    graph = generate_graph(
        n_chains,
        n_stores,
        primary_store_chain_weight,
        secondary_store_chain_edge,
        secondary_store_chain_weight,
        store_store_edge,
        store_store_weight,
        chain_chain_edge,
        chain_chain_weight,
    )

    graph.draw()

    # Optimisation
    partitions = initial_partition(graph.nodes_of_type(NODE_CHAIN), graph.edges())
    alpha = 1
    beta = 1

    lo_partitions, costs = local_optimisation(graph, partitions, alpha, beta)
    print(costs)

    T = 10
    r = 0.5
    sa_partitions, costs = simulated_annealing(graph, partitions, alpha, beta, T, r)
    print(costs)

    # Plot the partitions
    assert type(lo_partitions) == list
    for idx, p in enumerate(lo_partitions):
        assert type(p) == Partition
        for src, dst in p._edges:
            graph.set_edge_partition(src, dst, idx)

    graph.draw()
