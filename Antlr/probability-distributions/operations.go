package main

import (
	"math"
	"sort"
)

func Add(v1, v2 int) int {
	return v1 + v2
}

func Sub(v1, v2 int) int {
	return v1 - v2
}

func Mul(v1, v2 int) int {
	return v1 * v2
}

func Div(v1, v2 int) int {
	return v1 / v2
}

func CombineDistributions(dist1, dist2 Distribution,
	fn func(v1, v2 int) int) Distribution {

	result := Distribution{}

	for value1, prob1 := range dist1 {
		for value2, prob2 := range dist2 {
			x := fn(value1, value2)
			_, ok := result[x]
			if !ok {
				result[x] = prob1 * prob2
			} else {
				result[x] += prob1 * prob2
			}
		}
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
