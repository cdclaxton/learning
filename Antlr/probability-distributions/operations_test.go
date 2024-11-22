package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAdd(t *testing.T) {
	testCases := []struct {
		dist1    Distribution
		dist2    Distribution
		expected Distribution
	}{
		{
			dist1:    Distribution{2: 1.0},
			dist2:    Distribution{3: 1.0},
			expected: Distribution{5: 1.0},
		},
		{
			dist1:    Distribution{2: 0.2, 3: 0.8},
			dist2:    Distribution{3: 1.0},
			expected: Distribution{5: 0.2, 6: 0.8},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := CombineDistributions(testCase.dist1, testCase.dist2,
				Add)
			assert.True(t, distributionsEqual(actual, testCase.expected, 1e-6))
		})
	}
}

func TestSub(t *testing.T) {
	testCases := []struct {
		dist1    Distribution
		dist2    Distribution
		expected Distribution
	}{
		{
			dist1:    Distribution{3: 1.0},
			dist2:    Distribution{2: 1.0},
			expected: Distribution{1: 1.0},
		},
		{
			dist1:    Distribution{5: 0.2, 4: 0.8},
			dist2:    Distribution{3: 1.0},
			expected: Distribution{2: 0.2, 1: 0.8},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := CombineDistributions(testCase.dist1, testCase.dist2,
				Sub)
			assert.True(t, distributionsEqual(actual, testCase.expected, 1e-6))
		})
	}
}

func TestMul(t *testing.T) {
	testCases := []struct {
		dist1    Distribution
		dist2    Distribution
		expected Distribution
	}{
		{
			dist1:    Distribution{3: 1.0},
			dist2:    Distribution{2: 1.0},
			expected: Distribution{6: 1.0},
		},
		{
			dist1:    Distribution{5: 0.2, 4: 0.8},
			dist2:    Distribution{3: 1.0},
			expected: Distribution{15: 0.2, 12: 0.8},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := CombineDistributions(testCase.dist1, testCase.dist2,
				Mul)
			assert.True(t, distributionsEqual(actual, testCase.expected, 1e-6))
		})
	}
}

func TestUniqueValues(t *testing.T) {
	testCases := []struct {
		description   string
		distributions []Distribution
		expected      []int
	}{
		{
			description: "one distribution",
			distributions: []Distribution{
				{
					0: 0.1,
					1: 0.9,
				},
			},
			expected: []int{0, 1},
		},
		{
			description: "two distributions",
			distributions: []Distribution{
				{
					0: 0.1,
					1: 0.9,
				},
				{
					0: 0.1,
					2: 0.9,
				},
			},
			expected: []int{0, 1, 2},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual := uniqueValues(testCase.distributions...)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}

func TestNoisyMax(t *testing.T) {
	testCases := []struct {
		description string
		dists       []Distribution
		expected    Distribution
	}{
		{
			description: "one distribution",
			dists: []Distribution{
				{
					1: 0.4,
					2: 0.6,
				},
			},
			expected: Distribution{1: 0.4, 2: 0.6},
		},
		{
			description: "two distributions, two values",
			dists: []Distribution{
				{0: 0.2, 1: 0.8},
				{0: 0.3, 1: 0.7},
			},
			expected: Distribution{0: 0.06, 1: 0.94},
		},
		{
			description: "two distributions, three values",
			dists: []Distribution{
				{0: 0.2, 1: 0.7, 2: 0.1},
				{0: 0.3, 1: 0.7},
			},
			expected: Distribution{0: 0.06, 1: 0.84, 2: 0.1},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual := NoisyMax(testCase.dists...)
			assert.True(t, distributionsEqual(actual, testCase.expected, 1e-6))
		})
	}
}

func TestRemoveZeros(t *testing.T) {
	testCases := []struct {
		dist     Distribution
		expected Distribution
	}{
		{
			dist:     Distribution{1: 0.2, 2: 0.0, 3: 0.8},
			expected: Distribution{1: 0.2, 3: 0.8},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := removeZeros(testCase.dist)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}
