package main

import (
	"math"
	"sort"
)

// Distribution represents a discrete probability distribution.
type Distribution map[int]float64

// CumulativeProbability of the distribution for value x.
func (d Distribution) CumulativeProbability(x int) float64 {
	cumProb := 0.0

	for value, prob := range d {
		if value <= x {
			cumProb += prob
		}
	}

	return cumProb
}

// updateDistribution updates the original distribution with distribution dist
// where the probability of distribution dist is p.
func updateDistribution(original Distribution, p float64, dist Distribution) {
	for value, prob := range dist {
		existingProb := original[value]
		original[value] = existingProb + p*prob
	}
}

func NoisyMaxMixtureModelRecursive(probs []float64, dists []Distribution) Distribution {
	if len(probs) != len(dists) {
		panic("inconsistent number of probabilities and distributions")
	}

	// Number of distributions to combine
	N := len(probs)

	result := Distribution{}

	var generate func(int, float64, Distribution)
	generate = func(i int, sumLogProb float64, dist Distribution) {
		if i == N {
			// Add the distribution to the mixture model
			updateDistribution(result, math.Exp(sumLogProb), dist)
		} else {
			// State of distribution i is set to false
			generate(i+1, sumLogProb+math.Log(1-probs[i]), dist)

			// State of distribution i is set to true
			generate(i+1, sumLogProb+math.Log(probs[i]), NoisyMax(dist, dists[i]))
		}
	}

	generate(0, 0.0, Distribution{0: 1.0})

	return result
}

func integerAsBinary(i int, width int) []bool {
	result := make([]bool, width)

	for idx := width - 1; idx >= 0; idx-- {
		result[idx] = i&1 > 0
		i = i >> 1
	}

	return result
}

func NoisyMaxMixtureModelNonRecursive(probs []float64, dists []Distribution) Distribution {
	if len(probs) != len(dists) {
		panic("inconsistent number of probabilities and distributions")
	}

	// Set the output distribution for the case where all inputs have a state
	// set to false
	logP := 0.0
	for _, p := range probs {
		logP += math.Log(1 - p)
	}
	result := Distribution{0: math.Exp(logP)}

	// Number of inputs
	N := len(probs)

	// Number of combinations
	M := int(math.Pow(2, float64(N)))

	for i := 1; i < M; i++ {
		states := integerAsBinary(i, N)

		distsForRow := make([]Distribution, N)
		logP := 0.0
		for j := 0; j < N; j++ {
			if states[j] {
				distsForRow[j] = dists[j]
				logP += math.Log(probs[j])
			} else {
				distsForRow[j] = Distribution{0: 1.0}
				logP += math.Log(1 - probs[j])
			}
		}

		updateDistribution(result, math.Exp(logP), NoisyMax(distsForRow...))
	}

	return result
}

// uniqueValues within the distributions.
func uniqueValues(dists ...Distribution) []int {
	values := map[int]interface{}{}
	sliceValues := []int{}

	for _, dist := range dists {
		for value := range dist {
			_, ok := values[value]
			if !ok {
				values[value] = nil
				sliceValues = append(sliceValues, value)
			}
		}
	}

	// Sort the values to ensure consistency across runs
	sort.Slice(sliceValues, func(i, j int) bool {
		return sliceValues[i] < sliceValues[j]
	})

	return sliceValues
}

func NoisyMax(dists ...Distribution) Distribution {
	previousProb := 0.0
	result := Distribution{}

	for _, x := range uniqueValues(dists...) {
		currentProb := 0.0
		for _, dist := range dists {
			currentProb += math.Log(dist.CumulativeProbability(x))
		}
		currentProb = math.Exp(currentProb)

		result[x] = currentProb - previousProb
		previousProb = currentProb
	}

	return removeZeros(result)
}

// removeZeros from a distribution, where the value is zero.
func removeZeros(dist Distribution) Distribution {
	result := Distribution{}

	for value, prob := range dist {
		if prob > 0 {
			result[value] = prob
		}
	}

	return result
}
