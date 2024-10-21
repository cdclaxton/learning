package main

import (
	"fmt"
	"math"
	"math/rand"
	"reflect"
	"testing"
	"testing/quick"

	"github.com/stretchr/testify/assert"
)

// randomInteger in the range [min, max].
func randomInteger(min, max int) int {
	x := max - min + 1
	if x <= 0 {
		panic(fmt.Sprintf("randomInteger(%d, %d) isn't valid", min, max))
	}
	return rand.Intn(max-min+1) + min
}

// randomProbabilities generates n random probabilities.
func randomProbabilities(n int) []float64 {
	result := make([]float64, n)

	for i := 0; i < n; i++ {
		result[i] = rand.Float64()
	}

	return result
}

// randomDistribution returns a random distribution over the values.
func randomDistribution(values []int) Distribution {

	// Number of values in the distribution with non-zero probability
	numNonZeroValues := randomInteger(1, len(values))

	p := make([]float64, numNonZeroValues)
	total := 0.0
	for i := 0; i < numNonZeroValues; i++ {
		p[i] = rand.Float64()
		total += p[i]
	}

	// Normalise the distribution to sum to unity
	for i := 0; i < numNonZeroValues; i++ {
		p[i] = p[i] / total
	}

	rand.Shuffle(len(values), func(i, j int) {
		values[i], values[j] = values[j], values[i]
	})

	d := Distribution{}
	for i := 0; i < numNonZeroValues; i++ {
		d[values[i]] = p[i]
	}

	return d
}

func randomDistributions(n int, values []int) []Distribution {
	if n < 1 {
		panic(fmt.Sprintf("invalid n: %d", n))
	}

	dists := make([]Distribution, n)
	for i := 0; i < n; i++ {
		dists[i] = randomDistribution(values)
	}

	return dists
}

// distinctRandomIntegers returns a slice of random integers in the range
// [min, max] where the number of elements is a sample from a uniform
// distribution in the range [nMin, nMax].
func distinctRandomIntegers(nMin, nMax, min, max int) []int {

	// Random number of entries
	n := randomInteger(nMin, nMax)

	values := make([]int, 0, n)
	uniqueValues := map[int]interface{}{}

	for len(values) < n {
		x := randomInteger(min, max)
		_, ok := uniqueValues[x]
		if !ok {
			values = append(values, x)
			uniqueValues[x] = nil
		}
	}

	return values
}

func TestRandomInteger(t *testing.T) {
	minValue := 3
	maxValue := 5
	valueSeen := map[int]interface{}{}

	for i := 0; i < 100; i++ {
		value := randomInteger(minValue, maxValue)
		assert.True(t, minValue <= value && value <= maxValue)

		valueSeen[value] = nil
		if len(valueSeen) == 3 {
			break
		}
	}

	assert.Len(t, valueSeen, maxValue-minValue+1)
}

func TestRandomProbabilities(t *testing.T) {
	property := func(n int) bool {
		probs := randomProbabilities(n)

		if len(probs) != n {
			return false
		}

		for i := 0; i < n; i++ {
			if probs[i] < 0.0 || probs[i] > 1.0 {
				return false
			}
		}

		return true
	}

	config := quick.Config{
		MaxCount: 10,
		Values: func(v []reflect.Value, r *rand.Rand) {
			v[0] = reflect.ValueOf(r.Intn(20))
		},
	}

	assert.NoError(t, quick.Check(property, &config))
}

func TestRandomDistribution(t *testing.T) {
	property := func(values []int) bool {

		// Make a set of values
		setValues := map[int]interface{}{}
		for _, value := range values {
			setValues[value] = true
		}
		assert.Len(t, setValues, len(values))

		// Generate a random distribution
		dist := randomDistribution(values)

		// Check the values of the distribution and calculate the total
		// probability
		totalProb := 0.0
		for value, prob := range dist {
			_, ok := setValues[value]
			if !ok {
				return false
			}

			totalProb += prob
		}

		// Check the distribution sums to unity
		return math.Abs(totalProb-1.0) < 1e-6
	}

	config := quick.Config{
		MaxCount: 10,
		Values: func(v []reflect.Value, r *rand.Rand) {
			v[0] = reflect.ValueOf(distinctRandomIntegers(1, 10, 0, 15))
		},
	}

	assert.NoError(t, quick.Check(property, &config))
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

func distributionsEqual(actual, expected Distribution, tol float64) bool {
	if len(actual) != len(expected) {
		return false
	}

	for value, actualProb := range actual {
		expectedProb, ok := expected[value]
		if !ok || math.Abs(expectedProb-actualProb) > tol {
			return false
		}
	}

	return true
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

func TestUpdateDistribution(t *testing.T) {
	testCases := []struct {
		original Distribution
		p        float64
		dist     Distribution
		expected Distribution
	}{
		{
			original: Distribution{},
			p:        1.0,
			dist:     Distribution{2: 1.0},
			expected: Distribution{2: 1.0},
		},
		{
			original: Distribution{0: 0.2},
			p:        0.3,
			dist:     Distribution{2: 1.0},
			expected: Distribution{0: 0.2, 2: 0.3},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			updateDistribution(testCase.original, testCase.p,
				testCase.dist)
			assert.True(t, distributionsEqual(testCase.original, testCase.expected, 1e-6),
				"Expected distribution: %v, actual distribution: %v", testCase.expected, testCase.original)
		})
	}
}

func TestIntegerAsBinary(t *testing.T) {
	testCases := []struct {
		i        int
		width    int
		expected []bool
	}{
		{
			i:        0,
			width:    1,
			expected: []bool{false},
		},
		{
			i:        1,
			width:    1,
			expected: []bool{true},
		},
		{
			i:        0,
			width:    2,
			expected: []bool{false, false},
		},
		{
			i:        1,
			width:    2,
			expected: []bool{false, true},
		},
		{
			i:        2,
			width:    2,
			expected: []bool{true, false},
		},
		{
			i:        3,
			width:    2,
			expected: []bool{true, true},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := integerAsBinary(testCase.i, testCase.width)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}

func TestNoisyMaxMixtureModel(t *testing.T) {
	for i := 0; i < 100; i++ {
		numInputs := randomInteger(1, 3)

		// Random distributions
		values := distinctRandomIntegers(1, 5, 1, 10)
		dists := randomDistributions(numInputs, values)

		// Probability of each distribution
		probs := randomProbabilities(numInputs)

		// Noisy max mixture model calculation using two different approaches
		result1 := NoisyMaxMixtureModelRecursive(probs, dists)
		result2 := NoisyMaxMixtureModelNonRecursive(probs, dists)

		assert.True(t, distributionsEqual(result1, result2, 1e-6),
			"Recursive result: %v, non-recursive result: %v",
			result1, result2)
	}
}

func benchmarkTestSet() ([]float64, []Distribution) {
	p := []float64{0.1, 0.2, 0.3, 0.4, 0.5}
	dists := []Distribution{
		{
			0: 0.2,
			1: 0.8,
		},
		{
			1: 0.3,
			3: 0.7,
		},
		{
			0: 0.2,
			1: 0.7,
			2: 0.1,
		},
		{
			0: 0.15,
			1: 0.8,
			2: 0.05,
		},
		{
			1: 0.4,
			3: 0.6,
		},
	}

	return p, dists
}

// BenchmarkNonRecursive-2   	    5236	    287585 ns/op	   32296 B/op	     704 allocs/op
func BenchmarkNonRecursive(b *testing.B) {
	probs, dists := benchmarkTestSet()
	for i := 0; i < b.N; i++ {
		NoisyMaxMixtureModelNonRecursive(probs, dists)
	}
}

// BenchmarkRecursive-2   	    8210	    134042 ns/op	   12736 B/op	     344 allocs/op
func BenchmarkRecursive(b *testing.B) {
	probs, dists := benchmarkTestSet()
	for i := 0; i < b.N; i++ {
		NoisyMaxMixtureModelRecursive(probs, dists)
	}
}
