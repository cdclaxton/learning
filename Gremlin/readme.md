# Gremlin

## Download and install

```bash
wget https://dlcdn.apache.org/tinkerpop/3.7.1/apache-tinkerpop-gremlin-console-3.7.1-bin.zip
unzip apache-tinkerpop-gremlin-console-3.7.1-bin.zip
```

## Run

```bash
./apache-tinkerpop-gremlin-console-3.7.1/bin/gremlin.sh
```

## Notes

- Query language
- Navigates vertices and edges of a directed graph
- `TraversalSource` holds a reference to a `Graph` instance
- `TinkerGraph` is an in-memory graph database
- A `Traversal` is essentially an `Iterator`
- Model is a 'directed property graph'
- Properties are key-value pairs
- Vertices and edges can be given labels
- `label` and `id` are reserved attributes of vertices and edges

```
graph = TinkerFactory.createModern()
g = traversal().withEmbedded(graph)
```

- `g.V()` gets all vertices in the graph
- `g.V(1)` gets the vertex with unique identifier 1
- `g.V(1).values()` gets the values for vertex 1
- `g.V(1).values("name")` gets the 'name' property
- `g.V(1).outE("knows")` gets the edges with the label 'knows'
- `g.V(1).outE("knows").inV()` gets the vertices, equivalent to `g.V(1).out("knows")`
- `g.V(1).out("knows").values("name")`
- `g.V(1).out("knows").has("age", gt(30)).values("name")`
- `g.V().has("lang", "java")` gets all vertices with lang=java
- `g.V().has("person", "name", within("vadas", "marko"))` gets the vertices where the name is one of the list using the `within` comparator
- `g.V().has("person", "name", within("vadas", "marko")).values("age")` gets the 'age' property of the vertices
- `g.V().has("person", "name", within("vadas", "marko")).values("age").mean()` gets the mean age
- `g.V().has("person", "name", "marko").out("created").in("created").values("name")` finds people who worked on the software with Marko
- `g.V().has("person", "name", "marko").as("exclude").out("created").in("created").where(neq("exclude")).values("name")` finds the collaborators on the software with Marko
- `g.V().out().out()` traverses two steps
- `g.V().as("a").out().as("b").out().as("c").select("a", "b", "c")`
- `g.V().group().by(label)` groups all vertices by their vertex label and returns `==>[software:[v[3],v[5]],person:[v[1],v[2],v[4],v[6]]]`
- `g.V().group().by(label).by("name")` and returns `==>[software:[lop,ripple],person:[marko,vadas,josh,peter]]`

```
// Create a new graph
// 
//            weight=0.4
//            id=9
//            created=(label)
//  person  ---------->  software(=label)
//  id=1                 id=3
//  name=marko           name=lop
//  age=29               lang=java

graph = TinkerGraph.open()
g = traversal().withEmbedded(graph)

v1 = g.addV("person").property(id, 1).property("name", "marko").property("age", 29).next()

v2 = g.addV("software").property(id, 3).property("name", "lop").property("lang", "java").next()

g.addE("created").from(v1).to(v2).property(id, 9).property("weight", 0.4)
```

- `g.V().has("name", "marko")` can be improved to `g.V().has("person", "name", "marko")` by including the vertex label
- `g.V().has("person", "name", "marko").outE("created")` returns the edge
- `g.V().has("person", "name", "marko").outE("created").inV()` moves onto the vertex
- `g.V().has("person", "name", "marko").out("created")` returns the vertex
- `g.V().has("person", "name", "marko").out("created").values("name")` returns 'lop'

```
// Format of an edge in the console:
// e[9][1-created->3]
//   |  |    |     |
//   |  |    |    destination vertex
//   |  |   edge label
//   | source vertex
//   |
// edge ID
```

## Run a Groovy script

```bash
gremlin -e mycode.groovy
```

## Air routes data

Download from https://github.com/krlawrence/graph/blob/main/sample-data/air-routes.graphml

https://github.com/krlawrence/graph/blob/main/sample-data/air-routes-small.graphml

```bash
cd Gremlin

# Start Gremlin
./apache-tinkerpop-gremlin-console-3.7.1/bin/gremlin.sh -i load-air-routes-graph.groovy
```

```bash
./apache-tinkerpop-gremlin-console-3.7.1/bin/gremlin.sh
:load ../data/air-routes-small.graphml
:clear
g = graph.traversal()
```

```
// Count airports by country
g.V().hasLabel("airport").groupCount().by("country")

// Routes from MIA to HOU with two stops
g.V().has("code", "MIA").out().out().out().has("code", "HOU").path().by("code")

// Simplify using the repeat()
g.V().has("code", "MIA").repeat(out()).times(3).has("code", "HOU").path().by("code")

// Get vertices
g.V()

// Get edges
g.E()

// Get vertices with a given label
g.V().hasLabel("airport")

// Get vertices given a property
g.V().has("code", "DFW")

// Equivalent
g.V().hasLabel("airport").has("code", "DFW")
g.V().has("airport", "code", "DFW")

// Get property values of a given vertex
g.V().has("airport", "code", "DFW").values()

// Get a specific property of a given vertex
g.V().has("airport", "code", "DFW").values("code")

// Get multiple properties
g.V().has("airport", "code", "DFW").values("code", "runways")

// Find edges with a given property
g.E().has("dist")

// Find vertices with a given property
g.V().has("region")

// Find all vertices that don't have a given property
g.V().hasNot("region")
g.V().not(has("region"))

// Count the number of vertices
g.V().count()
g.V().hasLabel("airport").count()

// Number of outgoing edges with a given label
g.V().hasLabel("airport").outE("route").count()
g.E().hasLabel("route").count()

// Count the number of each type of vertex
g.V().groupCount().by(label)
g.V().label().groupCount()
g.V().group().by(label).by(count())

// Count the number of each type of edge
g.E().groupCount().by(label)
g.E().label().groupCount()

// Number of vertices with a given property
g.V().hasLabel("airport").groupCount().by("country")


```

- `.next()` is a terminal step (ends the graph traversal and returns a concrete object)
- `.next().getClass()`