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

import random

from distributions import *
from graph import *


def generate_graph(
    n_chains_gen,
    mean_n_stores_per_chain_gen,
    n_local_distributors_gen,
    n_in_country_distributors_gen,
    n_producers_gen,
    n_additional_gen,
    stores_connected,
):
    """Generate a random graph."""

    # Initialise the graph
    graph = Graph(allowed_connection_types)

    # Build the chains
    n_chains = n_chains_gen()
    for chain_index in range(n_chains):
        graph.add_node(f"C {chain_index}", NODE_CHAIN)

    # Build the stores
    n_stores = round(n_chains * mean_n_stores_per_chain_gen())
    for store_index in range(n_stores):
        graph.add_node(f"S {store_index}", NODE_STORE)

    # Connect the stores depending on the probability that any two stores are
    # connected
    store_nodes = graph.nodes_of_type(NODE_STORE)
    for i in range(len(store_nodes) - 1):
        if stores_connected() == 1:
            j = random.choice(list(range(i + 1, len(store_nodes))))
            graph.add_edge(store_nodes[i], store_nodes[j])

    # Connect the stores and the chains
    connect_nodes(graph, NODE_STORE, NODE_CHAIN)

    # Build the local distributors
    for local_distributor_index in range(n_local_distributors_gen()):
        graph.add_node(f"LD {local_distributor_index}", NODE_LOCAL_DISTRIBUTOR)

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

    return graph


if __name__ == "__main__":

    # Node-type specific distributions
    n_chains_gen = discrete_uniform(2, 4)
    mean_n_stores_per_chain_gen = continuous_uniform(2, 4)
    n_local_distributors_gen = discrete_uniform(1, 2)
    n_in_country_distributors_gen = discrete_uniform(2, 4)
    n_producers_gen = discrete_uniform(1, 2)
    n_additional_gen = discrete_uniform(10, 50)

    # Probability that two stores are connected
    p_two_stores_connected = continuous_uniform(0.1, 0.3)()
    stores_connected = bernoulli(p_two_stores_connected)

    # Generate a random graph
    graph = generate_graph(
        n_chains_gen,
        mean_n_stores_per_chain_gen,
        n_local_distributors_gen,
        n_in_country_distributors_gen,
        n_producers_gen,
        n_additional_gen,
        stores_connected,
    )

    # Plot the graph
    graph.draw()
