package dag

import (
	"fmt"
	"math/rand"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNodesWithNoIncomingEdges(t *testing.T) {
	testCases := []struct {
		edges    []Edge
		expected map[string]bool
	}{
		{
			// 1 --> 2
			edges: []Edge{
				{Source: "1", Destination: "2"},
			},
			expected: map[string]bool{"1": true},
		},
		{
			// 1 --> 2 --> 3
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
			},
			expected: map[string]bool{"1": true},
		},
		{
			// 1 --> 2 --> 3 (different order)
			edges: []Edge{
				{Source: "2", Destination: "3"},
				{Source: "1", Destination: "2"},
			},
			expected: map[string]bool{"1": true},
		},
		{
			// 1 --> 2 --|
			//           |--> 4
			// 3 --------|
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "4"},
				{Source: "3", Destination: "4"},
			},
			expected: map[string]bool{"1": true, "3": true},
		},
		{
			// 1 --> 2 --|
			//           |--> 4
			// 3 --------|
			edges: []Edge{
				{Source: "3", Destination: "4"},
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "4"},
			},
			expected: map[string]bool{"1": true, "3": true},
		},
		{
			// 1 --> 2
			//   <--
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "1"},
			},
			expected: map[string]bool{},
		},
		{
			// 1 --> 2 --> 3
			// ^           |
			// |-----------|
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
				{Source: "3", Destination: "1"},
			},
			expected: map[string]bool{},
		},
		{
			// 1--> 2 --> 3 ---|
			//      |          |---> 5
			//      |---> 4 ---|
			edges: []Edge{
				{Source: "3", Destination: "5"},
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "4"},
				{Source: "4", Destination: "5"},
				{Source: "2", Destination: "3"},
			},
			expected: map[string]bool{"1": true},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := nodesWithNoIncomingEdges(testCase.edges)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}

func TestNodeHasIncomingEdges(t *testing.T) {
	testCases := []struct {
		edges     []Edge
		edgeInUse []bool
		node      string
		expected  bool
	}{
		{
			// 1 --> 2
			edges: []Edge{
				{Source: "1", Destination: "2"},
			},
			edgeInUse: []bool{true},
			node:      "2",
			expected:  true,
		},
		{
			// 1 --> 2
			edges: []Edge{
				{Source: "1", Destination: "2"},
			},
			edgeInUse: []bool{true},
			node:      "1",
			expected:  false,
		},
		{
			// 1 --> 2 --> 3
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
			},
			edgeInUse: []bool{true, true},
			node:      "1",
			expected:  false,
		},
		{
			// 1 --> 2 --> 3
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
			},
			edgeInUse: []bool{true, true},
			node:      "2",
			expected:  true,
		},
		{
			// 1 -(x)-> 2 --> 3
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
			},
			edgeInUse: []bool{false, true},
			node:      "2",
			expected:  false,
		},
		{
			// 1 --> 2 --> 3
			//       |---> 4
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
				{Source: "2", Destination: "4"},
			},
			edgeInUse: []bool{true, true, true},
			node:      "1",
			expected:  false,
		},
		{
			// 1 --> 2 --> 3
			//       |---> 4
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
				{Source: "2", Destination: "4"},
			},
			edgeInUse: []bool{true, true, true},
			node:      "2",
			expected:  true,
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := nodeHasIncomingEdges(testCase.edges, testCase.edgeInUse, testCase.node)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}

func TestIsDag(t *testing.T) {
	testCases := []struct {
		edges    []Edge
		expected bool
	}{
		{
			// 1 --> 2
			edges: []Edge{
				{Source: "1", Destination: "2"},
			},
			expected: true,
		},
		{
			// 1 --> 2 --> 3
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
			},
			expected: true,
		},
		{
			// 1 --> 2 --|
			//           |--> 4
			// 3 --------|
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "4"},
				{Source: "3", Destination: "4"},
			},
			expected: true,
		},
		{
			// 1 --|        |--> 4
			//     |--> 3 --|
			// 2 --|        |--> 5
			edges: []Edge{
				{Source: "1", Destination: "3"},
				{Source: "2", Destination: "3"},
				{Source: "3", Destination: "4"},
				{Source: "3", Destination: "5"},
			},
			expected: true,
		},
		{
			// 1 --> 2 --|        |--> 5
			//           |--> 4 --|
			// 3 --------|        |--> 6
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "4"},
				{Source: "3", Destination: "4"},
				{Source: "4", Destination: "5"},
				{Source: "4", Destination: "6"},
			},
			expected: true,
		},
		{
			// 1 --> 2
			//   <--
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "1"},
			},
			expected: false,
		},
		{
			// 1 --> 2 --> 3
			// ^           |
			// |-----------|
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
				{Source: "3", Destination: "1"},
			},
			expected: false,
		},
		{
			// 1 --> 2 --> 3
			//       ^     |
			//       |-----|
			edges: []Edge{
				{Source: "1", Destination: "2"},
				{Source: "2", Destination: "3"},
				{Source: "3", Destination: "2"},
			},
			expected: false,
		},
		{
			// 1 --> 3 --> 4---> 5
			//       ^     |
			// 2 ----|     |---> 6
			edges: []Edge{
				{Source: "1", Destination: "3"},
				{Source: "2", Destination: "3"},
				{Source: "3", Destination: "4"},
				{Source: "4", Destination: "5"},
				{Source: "4", Destination: "6"},
			},
			expected: true,
		},
		{
			// 1 --> 3 --> 4---> 5 --|
			//       ^     |         |--> 7
			// 2 ----|     |---> 6 --|
			edges: []Edge{
				{Source: "1", Destination: "3"},
				{Source: "2", Destination: "3"},
				{Source: "3", Destination: "4"},
				{Source: "4", Destination: "5"},
				{Source: "4", Destination: "6"},
				{Source: "5", Destination: "7"},
				{Source: "6", Destination: "7"},
			},
			expected: true,
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {

			// Shuffle the edges
			rand.Shuffle(len(testCase.edges), func(i, j int) {
				testCase.edges[i], testCase.edges[j] = testCase.edges[j], testCase.edges[i]
			})

			actual := IsDag(testCase.edges)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}
