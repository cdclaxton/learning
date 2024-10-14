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
