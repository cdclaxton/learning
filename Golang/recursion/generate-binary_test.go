package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBitShiftPower(t *testing.T) {
	assert.Equal(t, 1, 1<<0)
	assert.Equal(t, 2, 1<<1)
	assert.Equal(t, 4, 1<<2)
}

func TestBinaryStrings(t *testing.T) {
	testCases := []struct {
		n        int
		expected []string
	}{
		{
			n:        0,
			expected: []string{},
		},
		{
			n:        1,
			expected: []string{"0", "1"},
		},
		{
			n:        2,
			expected: []string{"00", "01", "10", "11"},
		},
		{
			n: 3,
			expected: []string{
				"000",
				"001",
				"010",
				"011",
				"100",
				"101",
				"110",
				"111",
			},
		},
	}

	for _, testCase := range testCases {
		t.Run(fmt.Sprintf("n = %d", testCase.n), func(t *testing.T) {
			actual := BinaryStrings(testCase.n)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}
