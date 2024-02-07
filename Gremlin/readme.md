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
./gremlin-java8.bat -i C:\learning\Gremlin\load-air-routes-graph.groovy
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

// To investigate the structure of the graph
g.V().groupCount().by(label)
g.V().hasLabel("continent").out().groupCount().by(label)

// Number of airports in each continent
g.V().hasLabel("continent").group().by("code").by(out().count())

// Count the number of airports in a given set of countries
g.V().hasLabel("airport").groupCount().by("country").select("FR", "GR", "BE")

// Airports reachable from AUS
g.V().has("airport", "code", "AUS").out().values("code").fold()
g.V().has("airport", "code", "AUS").out("route").values("code").fold()

// Routes into LCY
g.V().has("airport", "code", "LCY").in("route").values("code").fold()

// US destinations from LHR
g.V().has("code", "LHR").out("route").has("country", "US").values("code").fold()

// Get path, e.g. [v[88],e[13696][88-route->74],v[74]]
g.V().has("airport", "code", "LCY").outE().inV().path()

// Get path without edge, e.g. [v[88],v[74]]
g.V().has("airport", "code", "LCY").out().path()

// Distance between airports from LCY, e.g. [LCY,780,MAD]
g.V().has("airport", "code", "LCY").outE().inV().path().by("code").by("dist")
g.V().has("airport", "code", "LCY").outE().inV().path().by("code").by("dist").by("code")
g.V().has("airport", "code", "LCY").outE().inV().path().by("code").by("dist").by("city")

// Number of runways at the airport reachable from LCY
g.V().has("airport", "code", "LCY").out().limit(5).values("runways").path().by("code").by("code").by()

// Code and city for source and destination
g.V().has("airport", "code", "AUS").out().limit(5).path().by(values("code", "city").fold())

// Number of routes out from source and destination
g.V().has("airport", "code", "BRI").out("route").limit(5).path().by(out().count().fold())

// Airports reachable from two hops from AUS
g.V().has("airport", "code", "AUS").out().out().path().by("code").limit(10)
g.V().has("code", "LHR").out().out().has("code", "PER").path().by("code").by("city").by("code")

// Return first and second hop airports only
g.V().has("airport", "code", "AUS").out().as("a").out().as("b").path().by("code").from("a").to("b").limit(10)
g.V().has("airport", "code", "AUS").out().as("a").out().as("b").path().by("code").from("a").limit(10)

// Check if a route exists between two airports
g.V().has("code", "AUS").out("route").has("code", "DFW").hasNext()

// Name a vertex and then select
g.V().has("code", "DFW").as("from").out().has("region", "US-CA").as("to").select("from", "to")
g.V().has("code", "DFW").as("from").out().has("region", "US-CA").as("to").select("from", "to").by("code")

// A point in a traversal can be given multiple names
g.V().has("type", "airport").limit(10).as("a", "b", "c").select("a", "b", "c").by("code").by("region").by(out().count())
g.V().has("type", "airport").limit(10).project("a", "b", "c").by("code").by("region").by(out().count())

// Give two parts of the traversal the same label
g.V(1).as("a").V(2).as("a").select("a")
g.V(1).as("a").V(2).as("a").select(first, "a")
g.V(1).as("a").V(2).as("a").select(last, "a")
g.V(1).as("a").V(2).as("a").select(all, "a")

g.V().has("code", "AUS").as("a").out().as("a").limit(10).select(last, "a").by("code").fold()

// Use unfold() as select(all) returns a list
g.V().has("code", "AUS").as("a").out().as("a").limit(10).select(all, "a").unfold().values("code").fold()

// Cities visited for a 2-stop trip from from Bristol to Sydney
g.V().has("code", "BRS").out().as("stop").out().as("stop").out().has("city", "Sydney").select(all, "stop").unfold().values("city").dedup().fold()

// Edge connecting two airports
g.V().has("code", "MIA").outE().as("e").inV().has("code", "DFW").select("e")
g.V().has("code", "MIA").outE().as("e").inV().has("code", "DFW").select("e").values("dist")

// Find routes from AUS to LHR, limiting to 10ms
g.V().has("airport", "code", "AUS").repeat(timeLimit(10).out()).until(has("code", "LHR")).path().by("code")

// Number of runways of airports in England
g.V().has("airport", "region", "GB-ENG").values("runways").dedup().fold()

// Nodes between 3 and 4
g.V(3).as("a").V(4).as("c").both().as("b").limit(10).select("a", "b", "c")

// Keys and values associated with a vertex (values are a list)
g.V().has("airport", "code", "PER").valueMap()
g.V().has("airport", "code", "PER").valueMap().unfold()

// Also include the ID and label of the vertex
g.V().has("airport", "code", "PER").valueMap(true).unfold()
g.V().has("airport", "code", "PER").valueMap().with(WithOptions.tokens).unfold()

// Request specific properties
g.V().has("airport", "code", "PER").valueMap(true, "runways").unfold()
g.V().has("airport", "code", "PER").valueMap().select("code", "runways")
g.V().has("airport", "code", "PER").valueMap("runways").with(WithOptions.tokens).unfold()
g.V().has("airport", "code", "PER").valueMap("runways").with(WithOptions.tokens, WithOptions.labels).unfold()
g.V().has("airport", "code", "PER").valueMap("runways").with(WithOptions.tokens, WithOptions.ids).unfold()

// Get the properties of an edge
g.V().has("airport", "code", "LHR").outE().as("a").inV().has("airport", "code", "EDI").select("a").valueMap(true)

// Unwrap the list of values
g.V().has("airport", "code", "PER").valueMap().by(unfold()).unfold()
g.V().has("airport", "code", "PER").elementMap().unfold()
g.V().has("airport", "code", "PER").elementMap("city").unfold()

// Get ID, label, properties, incoming and outgoing vertices of an edge
g.V().has("airport", "code", "LHR").outE().as("a").inV().has("airport", "code", "EDI").select("a").elementMap()

// Store properties for a vertex in a variable (don't forget the .next() step)
lhr = g.V().has("airport", "code", "LHR").valueMap().next()
println "The LHR airport is located in " + lhr['city'][0]

lhr = g.V().has("airport", "code", "LHR").elementMap().next()
println "The LHR airport is located in " + lhr['city']

// Returns results as a list
g.V().has("airport", "region", "GB-ENG").values("runways").toList().join(",")
g.V().has("airport", "region", "GB-ENG").values("runways").dedup().order().fold()

// Returns results as a set
g.V().has("airport", "region", "GB-ENG").values("runways").toSet()

// Weighted set includes a count of the number of each type
rs = g.V().has("airport", "region", "GB-ENG").values("runways").toBulkSet()
rs.uniqueSize() // number of unique values in the bulk set
rs.size()       // total number of values present
rs.asBulk()     // map of key-value pairs

// Store into a pre-existing variable
a = []
g.V().has("airport", "region", "GB-ENG").values("runways").fill(a)

s = [] as Set
g.V().has("airport", "region", "GB-ENG").values("runways").fill(s)

// Get the ID of a vertex
g.V().has("airport", "code", "PER").id()
g.V().hasId(62).values("code")  // returns PER
g.V().has(id,62).values("code")

// Vertices with ID in range
g.V().hasId(between(62,64)).values("code")
g.V().has(id, between(62,64)).values("code")

// Find routes from the vertex with ID 62 to any vertex with an ID less than 60
g.V().has(id, 62).out().has(id, lt(60)).path().by("code")

// Get the label for a vertex
g.V().has("code", "LBB").label()

// Airports in Australia
g.V().hasLabel("country").has("code", "AU").out("contains").values("code")
g.V().has("country", "code", "AU").out("contains").values("code")

// Reference a vertex label using label()
g.V().where(label().is(eq("airport"))).count()
g.V().has(label, "airport").count()
g.V().hasLabel("airport").count()

// Number of non-airport vertices
g.V().has(label, neq("airport")).count()
g.V().where(label().is(neq("airport"))).count()
g.V().not(hasLabel("airport")).count()

// Number of 'route' edges
g.E().has(label, "route").count()
g.E().where(label().is(eq("route"))).count()
g.E().hasLabel("route").count()

// Mean number of routes
g.V().hasLabel("airport").local(out("route").count()).mean()

// Ordered airports in Scotland (list of lists)
g.V().has("region", "GB-SCT").order().by("code").values("city", "code").fold()
g.V().has("region", "GB-SCT").order().by("code").local(values("code", "city").fold())

// Total number of runways
g.V().hasLabel("airport").values("runways").sum()

// Mean number of runways per airport
g.V().hasLabel("airport").values("runways").mean()

// Average number of airports to/from an airport
g.V().hasLabel("airport").local(both("route").count()).mean()

// Longest runway
g.V().hasLabel("airport").values("longest").max()
g.V().hasLabel("airport").has("longest", 18045).values()

// Most number of outgoing routes
g.V().hasLabel("airport").local(out("route").count()).max()

// Shortest continent name
g.V().hasLabel("continent").values("desc").min()

// Airports with at least 5 runways
g.V().has("runways", gte(5)).values("code", "city", "runways").fold()
g.V().has("runways", gte(5)).order().by("city").local(values("code", "city", "runways").fold())

// Airports with 3 runways
g.V().has("runways", 3).count()
g.V().values("runways").is(3).count()

// Airports with 4 <= runways <= 7
g.V().has("runways", inside(5,8)).values("code", "runways")

// Airports with 5 <= runways or runways >= 8
g.V().has("runways", outside(5,8)).values("runways").max()

// Airports with 3 <= runways <= 6
g.V().has("runways", within(3..6)).values("code", "runways").limit(14)

// Airports with 3 <= runways < 6
g.V().has("runways", between(3,6)).values("code", "runways").limit(14)

// Airports in Texas that are not Houston
g.V().has("airport", "region", "US-TX").has("city", neq("Houston")).local(values("code", "city").fold())

// Airports visitable from LHR in England and Scotland
g.V().has("airport", "code", "LHR").out().has("region", within("GB-ENG", "GB-SCT")).path().by("code")

// Airports visitable from LHR that are not in France or Germany
g.V().has("airport", "code", "LHR").out().has("country", without("FR", "DE")).values("code")

// Simulate a startsWith predicate (find cities starting with Bri)
g.V().hasLabel("airport").has("city", between("Bri", "Brj")).values("city")
g.V().hasLabel("airport").has("city", startingWith("Bri")).values("city")
g.V().hasLabel("airport").has("city", startingWith("Bri")).values("city").order().fold()

// Find codes starting with a single letter (works for capitalised names)
g.V().hasLabel("airport").has("code", between("X", "Xa")).values("code").fold()
g.V().hasLabel("airport").has("city", startingWith("X")).values("city")

// Cities ending in 'tol'
g.V().hasLabel("airport").has("city", endingWith("tol")).values("city")

// Cities containing 'sto'
g.V().hasLabel("airport").has("city", containing("sto")).values("city")

// Cities not starting with 'Ros'
g.V().hasLabel("airport").has("city", notStartingWith("Ros")).count()
g.V().hasLabel("airport").not(has("city", startingWith("Ros"))).count()

// Cities not ending in 'tol'
g.V().hasLabel("airport").has("city", notEndingWith("tol")).count()

// Cities not containing 'sto'
g.V().hasLabel("airport").has("city", notContaining("sto")).count()

// Routes from AUS to SYD avoiding LAX and DFW
g.V().has("airport", "code", "AUS").out().and(has("code", neq("LAX")), has("code", neq("DFW"))).out().has("code", "SYD").path().by("code")
g.V().has("airport", "code", "AUS").out().has("code", without("DFW", "LAX")).out().has("code", "SYD").path().by("code")

// Routes from LHR to DBX, stopping off in FR or DE
g.V().has("airport", "code", "LHR").out().has("country", within("FR", "DE")).out().has("code", "DXB").path().by("city")

// Randomly pick 20 airports
g.V().hasLabel("airport").coin(0.5).limit(20).values("code").fold()
g.V().hasLabel("airport").sample(20).values("code").fold()

// Pick airports with a probability of 0.05
g.V().hasLabel("airport").coin(0.05).local(values("code", "elev").fold()).fold()


```

- `.next()` is a terminal step (ends the graph traversal and returns a concrete object)
- `.next().getClass()`
- `out` outgoing adjacent vertices
- `in` incoming adjacent vertices
- `both` both incoming and outgoing adjacent vertices
- `outE` outgoing edges
- `inE` incoming edges
- `outV` outgoing vertex
- `inV` incoming vertex
- `bothE` both outgoing and incoming edges
- `otherV` vertex was not the vertex traversed from
- `hasNext` returns true or false

- `limit(n)` first n
- `tail(n)` last n
- `range(n, m)`
- `skip(n)` skips the first n
- `order`

- Statistical:

  - `count`
  - `min`
  - `max`

- Predicates to test values or ranges of values:

  - `eq` equal
  - `neq` not equal
  - `gt` greater than
  - `gte` greater than or equal
  - `lt` less than
  - `lte` less than or equal
  - `inside` a lower and upper bound
  - `outside` a lower and upper bound
  - `between`
  - `within` must match at least one of the values (range or list)
  - `without` must not match any of the values

- Text search predicates (case-sensitive):

  - `startingWith`
  - `endingWith`
  - `containing`
  - `notStartingWith`
  - `notEndingWith`
  - `notContaining`

- Modulators:

  - step that influences the behaviour of a step that it is associated with
  - e.g. `by`, `as`
  - processed in a round-robin fashion

- Anonymous traversal -- traversal inside a modulator, don't start with an E or V step
