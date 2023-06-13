package pairsfromset

import (
	"time"

	"golang.org/x/exp/maps"
)

// generateSet of numElements elements.
func generateSet(numElements int) map[int]bool {
	m := map[int]bool{}

	for i := 0; i < numElements; i++ {
		m[i] = true
	}

	return m
}

func expensiveOperation() {
	time.Sleep(1 * time.Millisecond)
}

func solution1(set map[int]bool) {

	// Convert the set to a slice
	elements := make([]int, len(set))
	for value := range set {
		elements[value] = value
	}

	// Walk through all pairs of elements
	for _, v1 := range elements {
		for _, v2 := range elements {
			if v1 == v2 {
				continue
			}

			expensiveOperation()
		}
	}
}

func solution2(set map[int]bool) {

	elements := maps.Keys(set)

	// Walk through all pairs of elements
	for _, v1 := range elements {
		for _, v2 := range elements {
			if v1 == v2 {
				continue
			}

			expensiveOperation()
		}
	}
}

func solution3(set map[int]bool) {

	for v1 := range set {
		for v2 := range set {
			if v1 == v2 {
				continue
			}

			expensiveOperation()
		}
	}
}
