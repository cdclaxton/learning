package dag

type Edge struct {
	Source      string
	Destination string
}

// nodesWithNoIncomingEdges returns nodes with no incoming edges.
func nodesWithNoIncomingEdges(edges []Edge) map[string]bool {

	// Potential nodes with no incoming edges
	potential := map[string]bool{}

	// Nodes with incoming edges
	hasIncoming := map[string]bool{}

	for _, edge := range edges {
		hasIncoming[edge.Destination] = true
		delete(potential, edge.Destination)

		if _, ok := hasIncoming[edge.Source]; !ok {
			potential[edge.Source] = true
		}
	}

	return potential
}

// element from a non-empty set
func element(s map[string]bool) (string, map[string]bool) {
	if len(s) == 0 {
		panic("Set is empty")
	}

	// Get the first element from the set
	var selected string
	for element := range s {
		selected = element
		break
	}

	delete(s, selected)
	return selected, s
}

// nodeHasIncomingEdges returns true if the node has incoming edges.
func nodeHasIncomingEdges(edges []Edge, edgeInUse []bool, node string) bool {

	for idx := range edges {
		if !edgeInUse[idx] {
			continue
		}

		if edges[idx].Destination == node {
			return true
		}
	}

	return false
}

func hasAnyEdges(edgesInUse []bool) bool {
	for _, inUse := range edgesInUse {
		if inUse {
			return true
		}
	}

	return false
}

// isDag returns true if the graph is acyclic using Kahn's algorithm.
func IsDag(edges []Edge) bool {

	// To avoid lots of memory swapping a slice is used to hold whether the edge
	// is still considered part of the graph
	edgeInGraph := make([]bool, len(edges))
	for idx := range edgeInGraph {
		edgeInGraph[idx] = true
	}

	// Set of all nodes with no incoming edges
	S := nodesWithNoIncomingEdges(edges)
	if len(S) == 0 {
		return false
	}

	// While the set S is not empty
	for len(S) > 0 {

		// Remove a node n from S
		var nodeN string
		nodeN, S = element(S)

		for idx := range edgeInGraph {
			if !edgeInGraph[idx] || edges[idx].Source != nodeN {
				continue
			}

			// Node m
			nodeM := edges[idx].Destination

			// Remove edge from the graph
			edgeInGraph[idx] = false

			if !nodeHasIncomingEdges(edges, edgeInGraph, nodeM) {
				S[nodeM] = true
			}
		}
	}

	return !hasAnyEdges(edgeInGraph)
}
