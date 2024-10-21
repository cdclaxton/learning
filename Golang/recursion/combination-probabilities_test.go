package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCombinationProbabilities(t *testing.T) {
	testCases := []struct {
		probabilities         []float64
		expectedCombinations  []string
		expectedProbabilities []float64
	}{
		{
			probabilities:        []float64{0.3},
			expectedCombinations: []string{"0", "1"},
			expectedProbabilities: []float64{
				0.7, // 0
				0.3, // 1
			},
		},
		{
			probabilities:        []float64{0.2, 0.3},
			expectedCombinations: []string{"00", "01", "10", "11"},
			expectedProbabilities: []float64{
				(1 - 0.2) * (1 - 0.3), // 00
				(1 - 0.2) * 0.3,       // 01
				0.2 * (1 - 0.3),       // 10
				0.2 * 0.3,             // 11
			},
		},
		{
			probabilities: []float64{0.9, 0.2, 0.4},
			expectedCombinations: []string{
				"000",
				"001",
				"010",
				"011",
				"100",
				"101",
				"110",
				"111",
			},
			expectedProbabilities: []float64{
				(1 - 0.9) * (1 - 0.2) * (1 - 0.4), // 000
				(1 - 0.9) * (1 - 0.2) * 0.4,       // 001
				(1 - 0.9) * 0.2 * (1 - 0.4),       // 010
				(1 - 0.9) * 0.2 * 0.4,             // 011
				0.9 * (1 - 0.2) * (1 - 0.4),       // 100
				0.9 * (1 - 0.2) * 0.4,             // 101
				0.9 * 0.2 * (1 - 0.4),             // 110
				0.9 * 0.2 * 0.4,                   // 111
			},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			combs, combProbs := CombinationProbabilities(testCase.probabilities)

			assert.Equal(t, testCase.expectedCombinations, combs)

			assert.Len(t, combProbs, len(testCase.expectedProbabilities))
			for idx := range testCase.expectedProbabilities {
				assert.InDelta(t, testCase.expectedProbabilities[idx],
					combProbs[idx], 1e-6)
			}
		})
	}
}
