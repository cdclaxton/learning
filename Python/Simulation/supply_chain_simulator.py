# Supply chain network simulator
#
# This script generates a synthetic supply chain where the following entity
# types are defined:
#
# store -- a shop that sells produce
# chain -- an overarching business that owns one or more stores
# local distributor -- a distributor within the country of the chain
# in-country distributor -- a distributor within the country of production
# producer -- a producer (generator) of a product
#
# Each of those nodes can be connected by any number of 'other' nodes, which
# model other types of businesses.

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns

from scipy import stats

# Node types
NODE_STORE = "store"
NODE_CHAIN = "chain"
NODE_LOCAL_DISTRIBUTOR = "local distributor"
NODE_IN_COUNTRY_DISTRIBUTOR = "in-country distributor"
NODE_PRODUCER = "producer"
NODE_OTHER = "other"

# Permitted connections between nodes given their type
allowed_connection_types = {
    NODE_STORE: [NODE_CHAIN, NODE_OTHER],
    NODE_CHAIN: [NODE_STORE, NODE_LOCAL_DISTRIBUTOR, NODE_OTHER],
    NODE_LOCAL_DISTRIBUTOR: [NODE_CHAIN, NODE_IN_COUNTRY_DISTRIBUTOR, NODE_OTHER],
    NODE_IN_COUNTRY_DISTRIBUTOR: [
        NODE_LOCAL_DISTRIBUTOR,
        NODE_PRODUCER,
    ],
    NODE_PRODUCER: [NODE_IN_COUNTRY_DISTRIBUTOR, NODE_OTHER],
    NODE_OTHER: [
        NODE_CHAIN,
        NODE_STORE,
        NODE_LOCAL_DISTRIBUTOR,
        NODE_IN_COUNTRY_DISTRIBUTOR,
        NODE_PRODUCER,
        NODE_OTHER,
    ],
}


def discrete_uniform(min_value, max_value):
    """Discrete uniform distribution in the range [min_value, max_value]."""
    dist = stats.randint(min_value, max_value + 1)

    def f():
        return dist.rvs()

    return f


def continuous_uniform(min_value, max_value):
    """Continuous uniform distribution in the range [min_value, max_value]."""
    dist = stats.uniform(min_value, max_value - min_value)

    def f():
        return dist.rvs()

    return f


def multinomial(p):
    """Multinomial distribution."""
    dist = stats.multinomial(n=1, p=p)

    def f():
        sample = dist.rvs()[0]
        return np.where(sample == 1)[0][0]

    return f


class Graph:
    def __init__(self, allowed_connection_types: dict[str, list[str]]):
        self._allowed_connection_types = allowed_connection_types

        self._G = nx.Graph()
        self._node_types: list[str] = []
        self._node_names: list[str] = []
        self._current_node_index = 0

    def add_node(self, name: str, node_type: str) -> int:
        """Add a node to the graph and return its node ID."""

        assert (
            node_type in self._allowed_connection_types
        ), f"Node type {node_type} isn't valid"

        self._node_names.append(name)
        self._node_types.append(node_type)
        self._G.add_node(self._current_node_index)
        self._current_node_index += 1

        return self._current_node_index - 1

    def add_edge(self, source: int, destination: int) -> None:
        """Add an edge from source to destination nodes."""

        # Check the nodes exist in the graph
        assert self._G.has_node(source), f"Node {source} doesn't exist"
        assert self._G.has_node(destination), f"Node {destination} doesn't exist"

        # Check the edge doesn't already exist
        assert not self._G.has_edge(
            source, destination
        ), f"Edge already exists {source} --- {destination}"

        # Check the nodes are allowed to be connected given their types
        source_node_type = self._node_types[source]
        destination_node_type = self._node_types[destination]
        assert source_node_type in self._allowed_connection_types
        assert (
            destination_node_type in self._allowed_connection_types[source_node_type]
        ), f"{source_node_type} -> {destination_node_type} connection not permitted"

        # All validation checks pass, so add the edge
        self._G.add_edge(source, destination)

    def assert_is_consistent(self):
        """Check that the graph is internally consistent."""

        assert len(self._G.nodes()) == len(
            self._node_types
        ), f"Expected {len(self._G.nodes())} nodes, got {len(self._node_types)}"

        assert len(self._G.nodes()) == len(
            self._node_names
        ), f"Expected {len(self._G.nodes())} nodes, got {len(self._node_names)}"

    def nodes(self) -> list[int]:
        """Returns a list of node IDs."""
        return list(self._G.nodes())

    def nodes_of_type(self, node_type: str) -> list[int]:
        """Returns a list of node IDs of type node_type."""
        return [i for i, tpe in enumerate(self._node_types) if tpe == node_type]

    def n_nodes_of_type(self, node_type: str) -> int:
        """Returns the number of nodes of a type node_type."""
        return len(self.nodes_of_type(node_type))

    def preferential_attachment_node(self) -> int:
        """Returns the node ID using preferential attachment."""

        # Probability distribution that a node is selected for preferential
        # attachment
        p_dist = np.array([degree for _, degree in self._G.degree()])
        p_dist = p_dist / np.sum(p_dist)

        # Sample from the probabilty distribution
        return multinomial(p_dist)()

    def draw(self):
        """Plot the graph."""

        # Build the labels for the nodes
        labeldict = {}
        for i in range(len(self._node_names)):
            labeldict[i] = f"{self._node_names[i]}"

        # Build the colours for the nodes
        palette = np.round(np.array(sns.color_palette("viridis", 2)) * 255).astype(int)
        rgb = ["#%02x%02x%02x" % (p[0], p[1], p[2]) for p in palette]
        node_colours = [
            rgb[0] if tpe != NODE_OTHER else rgb[1] for tpe in self._node_types
        ]

        nx.draw(self._G, node_color=node_colours, labels=labeldict, with_labels=True)
        plt.show()


def edges_to_connect_nodes(larger_list_nodes, smaller_list_nodes):
    """Returns the edges to connect nodes."""

    assert len(larger_list_nodes) >= len(smaller_list_nodes)

    edges = []

    # Ensure that the smaller_list_nodes are used at least once by tracking
    # whether they've been used
    smaller_nodes_used = [False for _ in range(len(smaller_list_nodes))]

    for node1 in larger_list_nodes:
        if all(smaller_nodes_used):
            node2 = random.choice(smaller_list_nodes)
        else:
            indices = [i for i, used in enumerate(smaller_nodes_used) if not used]
            idx = random.choice(indices)
            smaller_nodes_used[idx] = True
            node2 = smaller_list_nodes[idx]

        edges.append((node1, node2))

    return edges


def connect_nodes(graph: Graph, node_type1: str, node_type2: str):
    """Connect nodes of type node_type1 to nodes of type node_type2."""

    nodes_of_type1: list[int] = graph.nodes_of_type(node_type1)
    nodes_of_type2: list[int] = graph.nodes_of_type(node_type2)

    if len(nodes_of_type1) >= len(nodes_of_type2):
        edges = edges_to_connect_nodes(nodes_of_type1, nodes_of_type2)
    else:
        edges = edges_to_connect_nodes(nodes_of_type2, nodes_of_type1)

    for src, dst in edges:
        graph.add_edge(src, dst)


if __name__ == "__main__":

    # Node-type specific distributions
    n_chains_gen = discrete_uniform(2, 4)
    mean_n_stores_per_chain_gen = continuous_uniform(2, 4)
    n_local_distributors_gen = discrete_uniform(1, 2)
    n_in_country_distributors_gen = discrete_uniform(2, 4)
    n_producers_gen = discrete_uniform(1, 2)
    n_additional_gen = discrete_uniform(10, 50)

    # Initialise the graph
    graph = Graph(allowed_connection_types)

    # Build the chains
    n_chains = n_chains_gen()
    for chain_index in range(n_chains):
        graph.add_node(f"C {chain_index}", NODE_CHAIN)

    # Build the stores
    n_stores = round(n_chains * mean_n_stores_per_chain_gen())
    for store_index in range(n_stores):
        store_node = graph.add_node(f"S {store_index}", NODE_STORE)

    # Connect the stores and the chains
    connect_nodes(graph, NODE_STORE, NODE_CHAIN)

    # Build the local distributors
    for local_distributor_index in range(n_local_distributors_gen()):
        ld_node = graph.add_node(
            f"LD {local_distributor_index}", NODE_LOCAL_DISTRIBUTOR
        )

    # Connect the chains and the local distributors
    connect_nodes(graph, NODE_CHAIN, NODE_LOCAL_DISTRIBUTOR)

    # Build the in-country distributors
    for in_country_node_index in range(n_in_country_distributors_gen()):
        graph.add_node(f"ICD {in_country_node_index}", NODE_IN_COUNTRY_DISTRIBUTOR)

    # Connect the local distributors to the in-country distributors
    connect_nodes(graph, NODE_LOCAL_DISTRIBUTOR, NODE_IN_COUNTRY_DISTRIBUTOR)

    # Build the producers
    for producer_index in range(n_producers_gen()):
        graph.add_node(f"P {producer_index}", NODE_PRODUCER)

    # Connect the producers and the in-country distributors
    connect_nodes(graph, NODE_PRODUCER, NODE_IN_COUNTRY_DISTRIBUTOR)

    # Add the additional nodes and add an edge from the new additional node
    # to any other node
    for i in range(n_additional_gen()):
        additional_node_index = graph.add_node(f"{i}", NODE_OTHER)
        selected_node_index = graph.preferential_attachment_node()
        graph.add_edge(additional_node_index, selected_node_index)

    # Check the graph is consistent
    graph.assert_is_consistent()

    # Plot the graph
    graph.draw()
