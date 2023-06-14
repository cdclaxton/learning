package filechangedetection

import (
	"fmt"
	"path"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestChangeDetected(t *testing.T) {
	testCases := []struct {
		description string
		folder1     string
		folder2     string
		change      bool
	}{
		{
			description: "same file and content",
			folder1:     "test-1",
			folder2:     "test-1",
			change:      false,
		},
		{
			description: "same file, different content",
			folder1:     "test-1",
			folder2:     "test-2",
			change:      true,
		},
		{
			description: "different files",
			folder1:     "test-1",
			folder2:     "test-3",
			change:      true,
		},
		{
			description: "same files",
			folder1:     "test-3",
			folder2:     "test-3",
			change:      false,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			folder1 := path.Join("./test-data/", testCase.folder1)
			folder2 := path.Join("./test-data/", testCase.folder2)
			actual := ChangeDetected(folder1, folder2)
			assert.Equal(t, testCase.change, actual)
		})
	}
}

func TestSignaturesSame(t *testing.T) {
	testCases := []struct {
		sig1     FileSignatures
		sig2     FileSignatures
		expected bool
	}{
		{
			sig1: FileSignatures{
				"a": "100",
			},
			sig2: FileSignatures{
				"a": "100",
			},
			expected: true,
		},
		{
			sig1: FileSignatures{
				"a": "100",
			},
			sig2: FileSignatures{
				"a": "300",
			},
			expected: false,
		},
		{
			sig1: FileSignatures{
				"a": "100",
			},
			sig2: FileSignatures{
				"a": "100",
				"b": "200",
			},
			expected: false,
		},
		{
			sig1: FileSignatures{
				"a": "100",
				"b": "200",
			},
			sig2: FileSignatures{
				"a": "100",
				"b": "200",
			},
			expected: true,
		},
		{
			sig1: FileSignatures{
				"a": "100",
				"b": "500",
			},
			sig2: FileSignatures{
				"a": "100",
				"b": "200",
			},
			expected: false,
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := signaturesSame(testCase.sig1, testCase.sig2)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}

func TestGenerateSignatures(t *testing.T) {
	testCases := []struct {
		folder   string
		expected FileSignatures
	}{
		{
			folder: "./test-data/test-1",
			expected: FileSignatures{
				"a.txt": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
			},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.folder, func(t *testing.T) {
			actual := generateSignatures(testCase.folder)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}
