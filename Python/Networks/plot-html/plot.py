import json

import flask
import networkx as nx

# Create a graph of the form:
#
# A ---\
#      |---> D ---\
# B ---/          |---> E
#                 |
# C --------------/

# Define the list of nodes
nodes = ["A", "B", "C", "D", "E"]
edges = [
    ("A", "C"),
    ("B", "C"),
    ("D", "E"),
    ("C", "E"),
]

# Make a NetworkX graph from the edge list
G = nx.Graph()

for edge in edges:
    source, destination = edge
    source_idx = nodes.index(source)
    destination_idx = nodes.index(destination)

    G.add_edge(source_idx, destination_idx)

# Add labels
for node in G:
    G.nodes[node]["name"] = nodes[node]

print(f"Number of nodes = {G.number_of_nodes()}")
print(f"Number of edges = {G.number_of_edges()}")

# Write graph as JSON
d = nx.json_graph.node_link_data(G)
json.dump(d, open("force/graph.json", "w"))
print("Wrote node-edge JSON data to force/graph.json")

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="force")


@app.route("/")
def static_proxy():
    return app.send_static_file("force.html")


print("\nGo to http://localhost:8000 to see the network\n")
app.run(port=8000)