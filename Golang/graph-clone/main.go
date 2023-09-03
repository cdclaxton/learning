package main

import (
	"fmt"
	"log"
	"strings"
)

type Computation interface {
	Perform() int
}

type AddComputation struct{}

func (a *AddComputation) Perform() int {
	return 1
}

type PassThroughComputation struct{}

func (p *PassThroughComputation) Perform() int {
	return 2
}

type Node struct {
	Name   string
	Inputs []*Node
	Work   Computation
}

func (n *Node) Clone() Node {
	return Node{
		Name:   n.Name,
		Inputs: []*Node{},
	}
}

type Graph struct {
	Nodes []Node
}

// nodeIndex returns the index of a node given its name.
func (g *Graph) nodeIndex(nodeName string) (int, bool) {
	for idx, node := range g.Nodes {
		if node.Name == nodeName {
			return idx, true
		}
	}

	// The node could not be found
	return 0, false
}

// AddNode to the graph given its name.
func (g *Graph) AddNode(name string) {

	// Ensure the node doesn't already exist
	_, found := g.nodeIndex(name)
	if found {
		log.Fatalf("node already exists with name %s", name)
	}

	// Add a new node
	g.Nodes = append(g.Nodes, Node{
		Name:   name,
		Inputs: []*Node{},
	})
}

func (g *Graph) AddEdge(edge Edge) {
	sourceIdx, found := g.nodeIndex(edge.Source)
	if !found {
		log.Fatalf("source node %s not found", edge.Source)
	}

	destinationIdx, found := g.nodeIndex(edge.Destination)
	if !found {
		log.Fatalf("destination node %s not found", edge.Destination)
	}

	g.Nodes[destinationIdx].Inputs = append(g.Nodes[destinationIdx].Inputs,
		&g.Nodes[sourceIdx])
}

func (g *Graph) String() string {
	var sb strings.Builder

	sb.WriteString("Graph(")

	for _, node := range g.Nodes {

		a := -1
		if node.Work != nil {
			a = node.Work.Perform()
		}

		if len(node.Inputs) == 0 {
			continue
		}

		for _, inputNode := range node.Inputs {

			b := -1
			if inputNode.Work != nil {
				b = inputNode.Work.Perform()
			}

			sb.WriteString(fmt.Sprintf("%s[%d]--%s[%d]; ", inputNode.Name,
				a, node.Name, b))
		}
	}

	sb.WriteString(")")

	return sb.String()
}

// Clone the graph.
func (g *Graph) Clone() *Graph {
	g2 := Graph{
		Nodes: []Node{},
	}

	// Clone each of the nodes
	for _, originalNode := range g.Nodes {
		g2.Nodes = append(g2.Nodes, originalNode.Clone())
	}

	// Connect up the nodes
	for idx, originalNode := range g.Nodes {
		for _, originalNodeInput := range originalNode.Inputs {
			inputIdx, found := g.nodeIndex(originalNodeInput.Name)
			if !found {
				log.Fatalf("node with name %s not found", originalNodeInput.Name)
			}

			g2.Nodes[idx].Inputs = append(g2.Nodes[idx].Inputs, &g2.Nodes[inputIdx])
		}
	}

	return &g2
}

type Edge struct {
	Source      string
	Destination string
}

// buildGraph from an edge list.
func buildGraph(edges []Edge) *Graph {
	graph := Graph{
		Nodes: []Node{},
	}

	for _, edge := range edges {

		// Add the source node if required
		_, found := graph.nodeIndex(edge.Source)
		if !found {
			graph.AddNode(edge.Source)
		}

		// Add the destination node if required
		_, found = graph.nodeIndex(edge.Destination)
		if !found {
			graph.AddNode(edge.Destination)
		}

		// Add the connection
		graph.AddEdge(edge)
	}

	// Add computation based on a node's inputs
	for idx := range graph.Nodes {
		var comp Computation
		if len(graph.Nodes[idx].Inputs) > 1 {
			comp = &AddComputation{}
		} else {
			comp = &PassThroughComputation{}
		}
		graph.Nodes[idx].Work = comp
	}

	return &graph
}

func main() {
	// Build a graph from its edge list
	//
	// A --\
	//     |-- C --> D --\
	// B --/             |
	//                   |---> H
	// E ----------------|
	//                   |
	// F ---> G ---------/
	edgeList := []Edge{
		{
			Source:      "A",
			Destination: "C",
		},
		{
			Source:      "B",
			Destination: "C",
		},
		{
			Source:      "C",
			Destination: "D",
		},
		{
			Source:      "D",
			Destination: "H",
		},
		{
			Source:      "E",
			Destination: "H",
		},
		{
			Source:      "F",
			Destination: "G",
		},
		{
			Source:      "G",
			Destination: "H",
		},
	}

	graph := buildGraph(edgeList)

	for idx := range graph.Nodes {
		fmt.Printf("%s: %d\n", graph.Nodes[idx].Name,
			graph.Nodes[idx].Work.Perform())
	}

	fmt.Println(graph)

	// cloned := graph.Clone()
	// fmt.Println(cloned)
}
