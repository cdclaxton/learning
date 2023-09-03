# Graph scoring
#
# The graph is represented as a directed acyclic graph (DAG) where the nodes
# and edges can have properties. There can be multiple types of nodes and the
# type is simply an attribute in the properties.
#
# Node: identifier, properties (including type)
# Edge: identifier, properties

from __future__ import annotations
from dataclasses import dataclass
from typing import List


class Edge:
    """Graph edge."""
    
    def __init__(self, identifier: str, properties: dict, dst_node: Node):
        assert type(identifier) == str
        assert type(properties) == dict
        assert type(dst_node) == Node
        
        self.identifier = identifier
        self.properties = properties
        self.dst_node = dst_node

    def __repr__(self):
        return f"{self.identifier}; {self.properties}"

    def __str__(self):
        return self.__repr__()


class Node:
    """Graph node."""

    def __init__(self, identifier: str, properties: dict):
        assert type(identifier) == str
        assert type(properties) == dict
        
        self.identifier = identifier
        self.properties = properties

        self._children_edges: List[Edge] = []

    def __repr__(self):
        return f"{self.identifier}; {self.properties}"

    def __str__(self):
        return self.__repr__()    

    def add_edge(self, edge):
        """Add an edge to a child node."""
        assert isinstance(edge, Edge)
        self._children_edges.append(edge)


def nodes_with_properties(nodes: List[Node], properties: dict):
    """Extract nodes that contain the properties."""

    assert type(nodes) == list
    assert type(properties) == dict


if __name__ == '__main__':

    # Run tests
    n1 = Node("id-1", {"a": 12})
    n2 = Node("id-2", {"b": 10})
    print(n1)
    print(n2)

    e1 = Edge("e-1", {}, n2)
    n1.add_edge(e1)

    # Generate a graph


    # Perform scoring