package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRun(t *testing.T) {
	testCases := []struct {
		program        string
		description    string
		expectedMemory map[string]Distribution
	}{
		{
			program:     "a = {1:1.0}\n",
			description: "Single distribution, one element",
			expectedMemory: map[string]Distribution{
				"a": {1: 1.0},
			},
		},
		{
			program:     "a = {1:0.8, 2:0.2}\n",
			description: "Single distribution, two elements",
			expectedMemory: map[string]Distribution{
				"a": {1: 0.8, 2: 0.2},
			},
		},
		{
			program:     "a = {1:1.0}\nb = a\n",
			description: "Copy a distribution",
			expectedMemory: map[string]Distribution{
				"a": {1: 1.0},
				"b": {1: 1.0},
			},
		},
		{
			program:     "a = {1:1.0}\na = {2:1.0}\n",
			description: "Redefine a distribution",
			expectedMemory: map[string]Distribution{
				"a": {2: 1.0},
			},
		},
		{
			program:     "a = {1:1.0}\nb = {3:1.0}\nc = a + b\n",
			description: "Add two distributions",
			expectedMemory: map[string]Distribution{
				"a": {1: 1.0},
				"b": {3: 1.0},
				"c": {4: 1.0},
			},
		},
		{
			program:     "a = {5:0.2, 6:0.8}\nb = {3:1.0}\nc = a - b\n",
			description: "Subtract two distributions",
			expectedMemory: map[string]Distribution{
				"a": {5: 0.2, 6: 0.8},
				"b": {3: 1.0},
				"c": {2: 0.2, 3: 0.8},
			},
		},
		{
			program:     "a = {5:0.2, 6:0.8}\nb = {3:1.0}\nc = a * b\n",
			description: "Multiply two distributions",
			expectedMemory: map[string]Distribution{
				"a": {5: 0.2, 6: 0.8},
				"b": {3: 1.0},
				"c": {15: 0.2, 18: 0.8},
			},
		},
		{
			program:     "a = {10:0.2, 6:0.8}\nb = {2:1.0}\nc = a / b\n",
			description: "Divide two distributions",
			expectedMemory: map[string]Distribution{
				"a": {10: 0.2, 6: 0.8},
				"b": {2: 1.0},
				"c": {5: 0.2, 3: 0.8},
			},
		},
		{
			program:     "a = {0: 0.2, 1: 0.8}\nb = {0: 0.3, 1: 0.7}\nc = a | b\n",
			description: "Noisy Max of two distributions",
			expectedMemory: map[string]Distribution{
				"a": {0: 0.2, 1: 0.8},
				"b": {0: 0.3, 1: 0.7},
				"c": {0: 0.06, 1: 0.94},
			},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			result := run(testCase.program)
			assert.True(t, distributionsInTolerance(result, testCase.expectedMemory, 1e-6))
		})
	}
}
