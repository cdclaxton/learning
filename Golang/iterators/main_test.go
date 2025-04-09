package main

import (
	"slices"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestEdgeIterator(t *testing.T) {
	n1 := NewNode("node-1")
	n2 := NewNode("node-2")

	edge := NewEdge("edge-1", n1, n2)

	actual := slices.Collect(edge.Nodes())
	assert.Equal(t, []Node{n1, n2}, actual)

	// Get the first node
	firstNode := firstElement(edge.Nodes(), Node{})
	assert.Equal(t, n1, firstNode)
}

func buildTestGraph() (*Graph, []Node, []Edge) {
	// Build the graph
	//
	// n1 --> n2 <-- n3
	n1 := NewNode("node-1")
	n2 := NewNode("node-2")
	n3 := NewNode("node-3")

	e1 := NewEdge("1", n1, n2)
	e2 := NewEdge("2", n3, n2)

	g := NewGraph()
	g.AddEdge(e1)
	g.AddEdge(e2)

	return g, []Node{n1, n2, n3}, []Edge{e1, e2}
}

func TestGetEdges(t *testing.T) {
	g, _, edges := buildTestGraph()
	actual := slices.Collect(g.GetEdges())
	assert.Equal(t, edges, actual)
}

func TestGetUniqueNodes(t *testing.T) {
	g, nodes, _ := buildTestGraph()
	actual := slices.Collect(g.GetUniqueNodes())
	assert.Equal(t, nodes, actual)

	// Get the first unique node
	first := firstElement(g.GetUniqueNodes(), Node{})
	assert.Equal(t, nodes[0], first)
}

func TestGetNodesMatchingFilter(t *testing.T) {
	g, nodes, _ := buildTestGraph()
	filter := BuildFilterMatches("node-1")
	actual := slices.Collect(g.GetNodesMatchingFilter(filter))
	assert.Equal(t, []Node{nodes[0]}, actual)

	// Build a NodeFilter that is a logical AND of a two node filters
	f1 := BuildFilterStartsWith("node")
	f2 := BuildFilterEndsWith("2")
	filter2 := LogicalAndNodeFilters(f1, f2)
	actual2 := slices.Collect(g.GetNodesMatchingFilter(filter2))
	assert.Equal(t, []Node{nodes[1]}, actual2)

	// Get the first node matching the filter
	actual3 := firstElement(g.GetNodesMatchingFilter(filter2), Node{})
	assert.Equal(t, nodes[1], actual3)

	filter3 := LogicalAndNodeFilters(filter2, BuildFilterEndsWith("4"))
	actual3 = firstElement(g.GetNodesMatchingFilter(filter3), Node{})
	assert.Equal(t, Node{}, actual3)
}
