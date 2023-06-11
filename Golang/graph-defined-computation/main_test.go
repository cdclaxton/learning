package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSimpleData(t *testing.T) {
	sd := NewSimpleData()
	sd.AddValues("a", "a", "b")

	var s Data = sd
	assert.Equal(t, 2, s.NumberOfValues("a"))
	assert.Equal(t, 1, s.NumberOfValues("b"))
	assert.Equal(t, 0, s.NumberOfValues("c"))
}

func TestAddValues(t *testing.T) {
	var c Computation = AddValues{}
	result, err := c.Calculate([]int{1, 2, 3})
	assert.NoError(t, err)
	assert.Equal(t, 6, result)
	assert.Equal(t, "Add", c.GetName())
}

func TestMultiplyValues(t *testing.T) {
	var m Computation = MultiplyValues{}
	result, err := m.Calculate([]int{2, 2, 3})
	assert.NoError(t, err)
	assert.Equal(t, 12, result)
	assert.Equal(t, "Multiply", m.GetName())
}

func TestInstantiateComputation(t *testing.T) {
	c := NewComputeNode("a", false, AddComputation, nil)
	assert.NoError(t, c.InstantiateComputation())
	result, err := c.computation.Calculate([]int{1, 2, 3})
	assert.NoError(t, err)
	assert.Equal(t, 6, result)

	c = NewComputeNode("a", false, MultiplyComputation, nil)
	assert.NoError(t, c.InstantiateComputation())
	result, err = c.computation.Calculate([]int{2, 2, 3})
	assert.Equal(t, 12, result)
	assert.NoError(t, err)

	c = NewComputeNode("a", false, "unknown", nil)
	assert.Error(t, c.InstantiateComputation())
}

func TestExtractConstant(t *testing.T) {
	e := NewExtractConstant()

	var extractor Extractor = e
	err := extractor.Instantiate(map[string]string{
		ExtractorType:  ConstantExtractor,
		ExtractorValue: "3",
	})
	assert.NoError(t, err)

	sd := NewPopulatedSimpleData("a")
	result, err := extractor.Calculate(sd)
	assert.NoError(t, err)
	assert.Equal(t, 3, result)
}

func TestExtractNumValues(t *testing.T) {
	e := NewExtractNumValues()

	var extractor Extractor = e
	err := extractor.Instantiate(map[string]string{
		ExtractorType:  NumValuesExtractor,
		ExtractorValue: "a",
	})
	assert.NoError(t, err)

	sd := NewSimpleData()
	sd.AddValues("a", "a", "b")
	result, err := extractor.Calculate(sd)
	assert.NoError(t, err)
	assert.Equal(t, 2, result)

	err = e.Instantiate(map[string]string{
		"type": NumValuesExtractor,
	})
	assert.Error(t, err)
}

func TestExtractCount(t *testing.T) {
	e := NewExtractCount()

	var extractor Extractor = e
	err := extractor.Instantiate(map[string]string{
		ExtractorType: CountExtractor,
	})
	assert.NoError(t, err)

	sd := NewSimpleData()
	sd.AddValues("a", "a", "b")
	result, err := extractor.Calculate(sd)
	assert.NoError(t, err)
	assert.Equal(t, 3, result)
}

func TestSingleComputeNode(t *testing.T) {

	// Count extractor node
	node := NewComputeNode("a", true, "", map[string]string{
		ExtractorType: CountExtractor,
	})
	assert.NoError(t, node.Instantiate())

	sd := NewPopulatedSimpleData("a", "a", "b")
	result, err := node.Calculate(sd)
	assert.NoError(t, err)
	assert.Equal(t, 3, result)

	// Number of values extractor
	node = NewComputeNode("b", true, "", map[string]string{
		ExtractorType:  NumValuesExtractor,
		ExtractorValue: "a",
	})
	assert.NoError(t, node.Instantiate())

	result, err = node.Calculate(sd)
	assert.NoError(t, err)
	assert.Equal(t, 2, result)
}

// Test two compute nodes:
//
//	[node 0] ---> [node 1]
//	 count          add
func TestTwoComputeNodes(t *testing.T) {

	// Make node0 and node1
	node0 := NewComputeNode("node 0", true, "", map[string]string{
		ExtractorType: CountExtractor,
	})
	assert.NoError(t, node0.Instantiate())

	node1 := NewComputeNode("node 1", false, AddComputation, nil)
	assert.NoError(t, node1.Instantiate())

	// Connect node0 ---> node 1
	assert.NoError(t, node1.AddInput(node0))

	// Run calculation
	sd := NewPopulatedSimpleData("a", "a", "b")
	result, err := node1.Calculate(sd)
	assert.NoError(t, err)
	assert.Equal(t, 3, result)
}

// Test three compute nodes
//
//	      count
//		[node 0] --\
//		           |--> [node 2]
//		[node 1] --/      add
//	    numValues
func TestThreeComputeNodes(t *testing.T) {

	// Make nodes
	node0 := NewComputeNode("node 0", true, "", map[string]string{
		ExtractorType: CountExtractor,
	})
	assert.NoError(t, node0.Instantiate())

	node1 := NewComputeNode("node 1", true, "", map[string]string{
		ExtractorType:  NumValuesExtractor,
		ExtractorValue: "a",
	})
	assert.NoError(t, node1.Instantiate())

	node2 := NewComputeNode("node 2", false, AddComputation, nil)
	assert.NoError(t, node2.Instantiate())

	// Connect the nodes
	assert.NoError(t, node2.AddInput(node0))
	assert.NoError(t, node2.AddInput(node1))

	// Run calculation
	sd := NewPopulatedSimpleData("a", "a", "b")
	result, err := node2.Calculate(sd)
	assert.NoError(t, err)
	assert.Equal(t, 5, result)
}

func TestOutputNode(t *testing.T) {
	testCases := []struct {
		connections   []Connection
		expectedNode  string
		expectedError error
	}{
		{
			connections: []Connection{
				{
					Source:      "a",
					Destination: "b",
				},
			},
			expectedNode:  "b",
			expectedError: nil,
		},
		{
			connections: []Connection{
				{
					Source:      "a",
					Destination: "b",
				},
				{
					Source:      "b",
					Destination: "c",
				},
			},
			expectedNode:  "c",
			expectedError: nil,
		},
		{
			connections: []Connection{
				{
					Source:      "b",
					Destination: "c",
				},
				{
					Source:      "a",
					Destination: "b",
				},
			},
			expectedNode:  "c",
			expectedError: nil,
		},
		{
			connections: []Connection{
				{
					Source:      "a",
					Destination: "b",
				},
				{
					Source:      "b",
					Destination: "c",
				},
				{
					Source:      "c",
					Destination: "a",
				},
			},
			expectedNode:  "",
			expectedError: ErrInvalidGraph,
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprint(idx), func(t *testing.T) {
			actual, err := outputNode(testCase.connections)
			assert.ErrorIs(t, err, testCase.expectedError)
			assert.Equal(t, testCase.expectedNode, actual)
		})
	}
}

func TestLoadModel(t *testing.T) {
	testCases := []struct {
		filepath           string
		expectedOutputNode string
		expectedValue      int
	}{
		{
			filepath:           "./test-data/config-1.json",
			expectedOutputNode: "b",
			expectedValue:      2,
		},
		{
			filepath:           "./test-data/config-2.json",
			expectedOutputNode: "c",
			expectedValue:      4,
		},
	}

	sd := NewPopulatedSimpleData("a", "a", "b")

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %v", idx), func(t *testing.T) {

			// Load the model from JSON
			model, err := LoadModel(testCase.filepath)
			assert.NoError(t, err)
			assert.NotNil(t, model)

			// Check the output node
			assert.Equal(t, testCase.expectedOutputNode, model.outputNode.Name)

			// Run the computation on the model
			result, err := model.Compute(sd)
			assert.NoError(t, err)
			assert.Equal(t, testCase.expectedValue, result)
		})
	}
}
