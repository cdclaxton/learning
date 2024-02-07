conf = new BaseConfiguration()
conf.setProperty("gremlin.tinkergraph.vertexIdManager","LONG")
conf.setProperty("gremlin.tinkergraph.edgeIdManager","LONG")
conf.setProperty("gremlin.tinkergraph.vertexPropertyIdManager","LONG")
graph = TinkerGraph.open(conf)

graph.io(graphml()).readGraph('c:/learning/Gremlin/data/air-routes.graphml')

g=graph.traversal()
:set max-iteration 1000   