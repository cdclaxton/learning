import json
import flask
import networkx as nx

# Create a graph of the form:
#
# A ---\
#      |---> C ---\
# B ---/          |---> E
#                 |
# D --------------/

# Define the list of nodes
nodes = ["A", "B", "C", "D", "E"]
edges = [
    ("A", "C"),
    ("B", "C"),
    ("C", "E"),
    ("D", "E"),
]

# Create a representation for writing to JSON
output_edges = [
    {
        "source": nodes.index(source),
        "target": nodes.index(destination)
    } for source, destination in edges]

output_nodes = [
    {
        "name": node,
        "id": idx,
    } for idx, node in enumerate(nodes)]

d = {
    "nodes": output_nodes,
    "links": output_edges,
}

# Write graph as JSON
json.dump(d, open("force/graph.json", "w"))
print("Wrote node-edge JSON data to force/graph.json")

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="force")


@app.route("/")
def static_proxy():
    return app.send_static_file("force.html")


print("\nGo to http://localhost:8000 to see the network\n")
app.run(port=8000)