package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCorrectDistribution(t *testing.T) {
	testCases := []struct{
		description string
		dist DiscreteDistribution
		maxError float64
		expected DiscreteDistribution
		errorExpected error
	}{
		{
			description: "nil distribution",
			dist: nil,
			maxError: 1e-6,
			expected: nil,
			errorExpected: ErrNilDistribution,
		},
		{
			description: "empty distribution",
			dist: DiscreteDistribution{},
			maxError: 1e-6,
			expected: nil,
			errorExpected: ErrEmptyDistribution,
		},
		{
			description: "invalid max error",
			dist: DiscreteDistribution{0:1.0},
			maxError: -0.1,
			expected: nil,
			errorExpected: ErrInvalidMaxError,
		},
		{
			description: "one element, within range",
			dist: DiscreteDistribution{0:1.0},
			maxError: 1e-6,
			expected: DiscreteDistribution{0:1.0},
			errorExpected: nil,
		},
		{
			description: "one element, at top of range",
			dist: DiscreteDistribution{0:1.0 + 1e-6},
			maxError: 1e-6,
			expected: DiscreteDistribution{0:1.0},
			errorExpected: nil,
		},
		{
			description: "one element, outside upper range",
			dist: DiscreteDistribution{0:1.12},
			maxError: 0.1,
			expected: nil,
			errorExpected: ErrTotalOutsidePermittedRange,
		},
		{
			description: "one element, below range",
			dist: DiscreteDistribution{0: 1.0 - 0.5e-6},
			maxError: 1e-6,
			expected: DiscreteDistribution{0:1.0},
			errorExpected: nil,
		},
		{
			description: "two elements, total = 1",
			dist: DiscreteDistribution{0:0.3, 1:0.7},
			maxError: 1e-6,
			expected: DiscreteDistribution{0:0.3, 1:0.7},
			errorExpected: nil,
		},
		{
			description: "two elements, total < 1",
			dist: DiscreteDistribution{0:0.3, 1:0.6},
			maxError: 0.1,
			expected: DiscreteDistribution{
				0:0.3 / (0.3 + 0.6), 
				1:0.6 / (0.3 + 0.6),
			},
			errorExpected: nil,
		},
		{
			description: "two elements, both differ by maxError",
			dist: DiscreteDistribution{0:0.2, 1:0.6},
			maxError: 0.1,
			expected: DiscreteDistribution{
				0:0.2 / (0.2 + 0.6), 
				1:0.6 / (0.2 + 0.6),
			},
			errorExpected: nil,
		},
		{
			description: "two elements, total > 1",
			dist: DiscreteDistribution{0:0.3, 1:0.81},
			maxError: 0.1,
			expected: DiscreteDistribution{
				0: 0.3 / (0.3 + 0.81),
				1: 0.81 / (0.3 + 0.81),
			},
			errorExpected: nil,
		},
		{
			description: "two elements, negative prob in range",
			dist: DiscreteDistribution{0:-0.05, 1:1.1},
			maxError: 0.1,
			expected: DiscreteDistribution{
				0: 0.05 / (0.05 + 1.1),
				1: 1.1 / (0.05 + 1.1),
			},
			errorExpected: nil,
		},
		{
			description: "two elements, prob outside range",
			dist: DiscreteDistribution{0:-0.11, 1:1.0 - 0.11},
			maxError: 0.1,
			expected: nil,
			errorExpected: ErrValueOutsidePermittedRange,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual, err := correctDistribution(testCase.dist, testCase.maxError)
			assert.ErrorIs(t, err, testCase.errorExpected)
			assert.True(t, testCase.expected.Equal(actual))
		})
	}
}