package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func benchmarkCollectResults(numNodes int, b *testing.B) {
	nodes := makeNodes(numNodes)
	for i := 0; i < b.N; i++ {
		x := collectResults(nodes)
		assert.Equal(b, numNodes, len(x))
	}
}

func BenchmarkCollectResults10(b *testing.B) {
	benchmarkCollectResults(10, b)
}

func BenchmarkCollectResults20(b *testing.B) {
	benchmarkCollectResults(20, b)
}

func BenchmarkCollectResults50(b *testing.B) {
	benchmarkCollectResults(50, b)
}

func benchmarkCollectResults2(numNodes int, b *testing.B) {
	nodes := makeNodes(numNodes)
	for i := 0; i < b.N; i++ {
		x := collectResults2(nodes)
		assert.Equal(b, numNodes, len(x))
	}
}

func BenchmarkCollectResults2_10(b *testing.B) {
	benchmarkCollectResults2(10, b)
}

func BenchmarkCollectResults2_20(b *testing.B) {
	benchmarkCollectResults2(20, b)
}

func BenchmarkCollectResults2_50(b *testing.B) {
	benchmarkCollectResults2(50, b)
}