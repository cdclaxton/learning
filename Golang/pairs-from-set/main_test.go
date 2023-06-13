package pairsfromset

import "testing"

const numElementsInSet = 25

func BenchmarkSolution1(b *testing.B) {

	// Generate the set
	elements := generateSet(numElementsInSet)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		solution1(elements)
	}
}

func BenchmarkSolution2(b *testing.B) {

	// Generate the set
	elements := generateSet(numElementsInSet)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		solution2(elements)
	}
}

func BenchmarkSolution3(b *testing.B) {

	// Generate the set
	elements := generateSet(numElementsInSet)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		solution3(elements)
	}
}
