package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSimpleMax(t *testing.T) {

	// Check the function panics when there are no values
	assert.Panics(t, func() {
		simpleMax([]int{})
	})

	// Check a slice of ints
	values := []int{1, 4, 2}
	assert.Equal(t, 4, simpleMax(values))

	// Check a slice of floats
	values2 := []float64{2.3, 6.2, 9.0}
	assert.Equal(t, 9.0, simpleMax(values2))
}

func TestMean(t *testing.T) {
	assert.InDelta(t, 4.0, mean([]float64{2.0, 6.0}), 1e-5)
	assert.InDelta(t, 4.0, mean([]int{2, 6}), 1e-5)
}

func TestGetAction(t *testing.T) {
	m := NewMessage("id-1", "Add")
	assert.Equal(t, Action("Add"), getAction(m))
}

func TestUpperCase(t *testing.T) {
	assert.Equal(t, "ADD", upperCase("Add"))
	assert.Equal(t, "ADD", upperCase(Action("add")))
}
