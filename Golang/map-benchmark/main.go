// Run tests with:
// go test -run=XXX -bench=.

package main

import "fmt"

// DiscreteDistribution represents a sparse discrete probability distribution
type DiscreteDistribution map[float64]float64

type ProbabilisticNode struct {
	name string
	dist DiscreteDistribution
}

func makeNodes(numNodes int) []ProbabilisticNode {
	nodes := make([]ProbabilisticNode, numNodes)

	for i := 0; i < numNodes; i++ {
		nodes[i] = ProbabilisticNode{
			name: fmt.Sprintf("Node %d", i),
			dist: DiscreteDistribution{
				0.0: 0.5,
				1.0: 0.2,
				4.0: 0.2,
				10.0: 0.1,
			},
		}
	}

	return nodes
}

func collectResults(nodes []ProbabilisticNode) map[string]DiscreteDistribution {
	result := map[string]DiscreteDistribution{}

	for _, node := range nodes {
		result[node.name] = node.dist
	}

	return result
}

func collectResults2(nodes []ProbabilisticNode) map[string]DiscreteDistribution {
	result := make(map[string]DiscreteDistribution, len(nodes))

	for _, node := range nodes {
		result[node.name] = node.dist
	}

	return result
}