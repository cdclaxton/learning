package main

import (
	"iter"
	"strings"
)

type Node struct {
	Id string
}

func NewNode(id string) Node {
	return Node{
		Id: id,
	}
}

type Edge struct {
	Id  string
	Src Node // Source node
	Dst Node // Destination node
}

func NewEdge(id string, src Node, dst Node) Edge {
	return Edge{
		Id:  id,
		Src: src,
		Dst: dst,
	}
}

// Nodes iterator.
func (e Edge) Nodes() iter.Seq[Node] {
	return func(yield func(Node) bool) {
		if !yield(e.Src) {
			return
		}

		if !yield(e.Dst) {
			return
		}
	}
}

type Graph struct {
	Edges []Edge
}

func NewGraph() *Graph {
	return &Graph{
		Edges: []Edge{},
	}
}

func (g *Graph) AddEdge(e Edge) {
	g.Edges = append(g.Edges, e)
}

func (g *Graph) GetEdges() iter.Seq[Edge] {
	return func(yield func(Edge) bool) {
		for _, edge := range g.Edges {
			if !yield(edge) {
				return
			}
		}
	}
}

func (g *Graph) GetUniqueNodes() iter.Seq[Node] {
	nodes := map[Node]any{}

	return func(yield func(Node) bool) {
		for edge := range g.GetEdges() {
			for node := range edge.Nodes() {
				_, ok := nodes[node]
				if !ok && !yield(node) {
					return
				}
				nodes[node] = nil
			}
		}
	}
}

func firstElement[T any](seq iter.Seq[T], emptyCase T) T {
	for element := range seq {
		return element
	}

	return emptyCase
}

type NodeFilter func(node Node) bool

func BuildFilterMatches(id string) NodeFilter {
	return func(node Node) bool {
		return node.Id == id
	}
}

func BuildFilterStartsWith(s string) NodeFilter {
	return func(node Node) bool {
		return strings.HasPrefix(node.Id, s)
	}
}

func BuildFilterEndsWith(s string) NodeFilter {
	return func(node Node) bool {
		return strings.HasSuffix(node.Id, s)
	}
}

func LogicalAndNodeFilters(filters ...NodeFilter) NodeFilter {
	return func(node Node) bool {
		for _, f := range filters {
			if !f(node) {
				return false
			}
		}
		return true
	}
}

func (g *Graph) GetNodesMatchingFilter(filter NodeFilter) iter.Seq[Node] {
	return func(yield func(Node) bool) {
		for node := range g.GetUniqueNodes() {
			if filter(node) && !yield(node) {
				return
			}
		}
	}
}
