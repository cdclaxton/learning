# Graph-defined probabilistic computation 
#
# G = object on which computation is performed (e.g. a graph or tree or a set
# of two or more objects). It is assumed there is only one G object for a given 
# computation. 
# 
# The function f_k() where k = 0, 1, ..., K-1 is a feature extractor. It
# operates on the input and generates a vector of integers (counts) V_k.
#
# V_k = f_k(G)
#
# For the purposes of the experiment, G is defined as a dict with properties 
# that will be used by the f_k() functions. Function f_k() access the kth 
# property of the dict G, i.e. f_k = G[k].
#
# The function d_k(V_k) converts the feature vector V_k to a probability
# distribution. If the functions d_k() where k = 0, 1, ..., K-1 are such that
# the same operation is performed, but with different configuration, then
# 
# d_k(V_k) = d(V_k, c_k)
#
# where c_k is the configuration for the kth function.
#
# For two functions h_0 and h_1 then the above can be represented as:
#
#     [ X_0 = d(V_0, c_0) ]       [ X_1 = d(V_1, c_1) ]     prob. dists
#               ^                           ^
#               |                           |
#        [ V_0 = f_0(G) ]            [ V_1 = f_1(G) ]       vector of ints
#
# Requirements:
# - Build the computation graph once and use for multiple runs (with different
#   input graphs G) to improve efficiency compared to building the computation
#   graph for each run.
# - Feature extractor functions f() will be defined in code and referenced by
#   name in config.
# - Probability distribution will be modelled as a dict to provide a sparse
#   representation.

from collections import defaultdict
from functools import partial

def build_f_fns(K):
    """Build each function f_k where k = 0, ..., K-1."""
    assert K > 0
    return [lambda x, v=i: x[v] for i in range(K)]


def d(V, c):
    """Function to generate a probability distribution."""

    assert type(c) == list
    assert len(c) == 2
    assert type(V) == list
    assert all([type(vi) == int for vi in V])

    result = defaultdict(int)
    for idx, value in enumerate(V):
        if value > 0:
            centre = idx * c[0] + c[1]
            result[centre] += value * 0.8
            result[centre - 1] += value * 0.1
            result[centre + 1] += value * 0.1

    result = dict(result)

    # Normalise the values
    total = sum(result.values())
    result = {k:(v/total) for k,v in result.items()}

    # Return the probability distribution
    assert type(result) == dict
    assert abs(sum(result.values()) - 1.0) < 1e-5
    return result


def prob_distribution_valid(dist):
    """Is the (sparse) probability distribution valid?"""

    assert type(dist) == dict
    return (sum(dist.values()) - 1.0) < 1e-5 and \
        all([type(k) == float or type(k) == int for k in dist.keys()])


def dist_sum_two_rvs(x, y):
    """Distribution of the sum of two random variables."""

    assert prob_distribution_valid(x)
    assert prob_distribution_valid(y)

    result = defaultdict(int)

    for key1 in x.keys():
        for key2 in y.keys():
            total = key1 + key2
            result[total] += x[key1] * y[key2]

    result = dict(result)

    assert prob_distribution_valid(result)
    return result


def dist_sum_of_rvs(dists):
    """Distribution of the sum of random variables."""

    assert len(dists) >= 2
    assert all([prob_distribution_valid(d) for d in dists])

    # Distribution of the sum of the first two random variables
    result = dist_sum_two_rvs(dists[0], dists[1])

    for idx in range(2, len(dists)):
        result = dist_sum_two_rvs(result, dists[idx])

    assert prob_distribution_valid(result)
    return result


def dist_prod_two_rvs(x, y):
    """Distribution of the product of two random variables."""

    assert prob_distribution_valid(x)
    assert prob_distribution_valid(y)

    result = defaultdict(int)

    for key1 in x.keys():
        for key2 in y.keys():
            total = key1 * key2
            result[total] += x[key1] * y[key2]

    result = dict(result)

    assert prob_distribution_valid(result)
    return result


def dist_prod_of_rvs(dists):
    """Distribution of the product of random variables."""

    assert len(dists) >= 2
    assert all([prob_distribution_valid(d) for d in dists])

    # Distribution of the product of the first two random variables
    result = dist_prod_two_rvs(dists[0], dists[1])

    for idx in range(2, len(dists)):
        result = dist_prod_two_rvs(result, dists[idx])

    assert prob_distribution_valid(result)
    return result


class Node:
    def __init__(self, name):
        assert type(name) == str and len(name) > 0

        self.name = name
        self.parents = []
        self.prob_dist = None

    def add_parent(self, parent):
        assert isinstance(parent, Node)
        assert parent not in self.parents
        self.parents.append(parent)

    def calculate(self):
        assert False, "Unimplemented"


class FDNode(Node):
    """Feature extractor and distribution generating node."""
    def __init__(self, name, extractor_fn, dist_fn):
        super().__init__(name)
        self.extractor_fn = extractor_fn
        self.dist_fn = dist_fn
        self.input = None

    def set_input(self, input):
        self.input = input
    
    def calculate(self):
        """Perform feature extraction and prob. dist. calculation."""

        if self.prob_dist is None:
            assert self.input is not None
            v = self.extractor_fn(self.input)
            d = self.dist_fn(v)
            assert prob_distribution_valid(d)
            self.prob_dist = d
        
        return self.prob_dist


class MNode(Node):
    """Mathematical combination of random variables."""
    def __init__(self, name, fn):
        super().__init__(name)
        self.fn = fn

    def calculate(self):
        if self.prob_dist is None:
            probs = [p.calculate() for p in self.parents]
            d = self.fn(probs)
            assert prob_distribution_valid(d)
            self.prob_dist = d

        return self.prob_dist


def build_fd_node(config):
    """Build an FDNode."""
    return FDNode(config['name'], config['extractor-fn'], config['dist-fn'])

def build_m_node(config):
    """Build an MNode."""
    return MNode(config['name'], config['fn'])

def find_node_by_name(nodes, name):
    """Find a node in a list of nodes based on the node's name."""
    assert type(nodes) == list
    assert all([isinstance(n, Node) for n in nodes]) 
    assert type(name) == str

    for n in nodes:
        if n.name == name:
            return n

    return None

def connect_nodes(nodes, parent_name, child_name):
    """Connect a child node to its parents based on their name."""
    assert type(nodes) == list
    assert all([isinstance(n, Node) for n in nodes]) 
    assert type(parent_name) == str
    assert type(child_name) == str

    parent_node = find_node_by_name(nodes, parent_name)
    assert parent_node is not None

    child_node = find_node_by_name(nodes, child_name)
    assert child_node is not None

    child_node.add_parent(parent_node)

def set_parents_of_node(nodes, node_name, parents):
    for p in parents:
        connect_nodes(nodes, p, node_name)
    
def build_graph(config):
    """Build graph from config."""

    # Build the nodes
    nodes = [build_fd_node(node_config) for node_config in config['fd-nodes']]
    nodes.extend([build_m_node(node_config) for node_config in config['m-nodes']])

    # Connect up the nodes (only MNodes have parents)
    for node_config in config['m-nodes']:
        set_parents_of_node(nodes, node_config['name'], node_config['parents'])        

    return nodes
    

if __name__ == '__main__':

    # Define the h_k functions
    K = 2
    f_fns = build_f_fns(K)

    # Define the f_j functions
    d_0 = partial(d, c=[1, 1])
    d_1 = partial(d, c=[1, 2])

    # Dict representation of the graph structure (will come from JSON)
    structure = {
        "fd-nodes": [
            {
                "name": "fd_0",
                "extractor-fn": f_fns[0],
                "dist-fn": d_0
            },
            {
                "name": "fd_1",
                "extractor-fn": f_fns[1],
                "dist-fn": d_1
            }
        ],
        "m-nodes": [
            {
                "name": "m_0",
                "fn": dist_sum_of_rvs,
                "parents": ["fd_0", "fd_1"]
            }
        ],
        "execution-order": ["fd_0", "fd_1", "m_0"]
    }

    nodes = build_graph(structure)

    # Data structure to represent the object that is subject to feature
    # extraction
    G = {
        0: [0, 1, 0],
        1: [1, 0, 1]
    }

    # Set the input to each node that is a feature extractor and probability
    # distribution creator
    for n in nodes:
        if type(n) == FDNode:
            n.set_input(G)

    # Calculate the probability distribution of each node given the defined
    # execution order
    for node_name in structure['execution-order']:
        node = find_node_by_name(nodes, node_name)
        assert isinstance(node, Node)
        print(f"Node: {node.name}, Dist: {node.calculate()}")

