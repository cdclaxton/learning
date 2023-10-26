package main

import (
	"fmt"
	"math"
)

// occurrenceProbability of a sequence with nPresent tokens in the sequence and
// nMissing tokens absent. The probability of a missing token is pMissing.
func occurrenceProbability(nPresent int, nMissing int, pMissing float64) (float64, error) {

	if pMissing < 0.0 || pMissing > 1.0 {
		return 0.0, fmt.Errorf("invalid probability: %f", pMissing)
	}

	return math.Pow(1-pMissing, float64(nPresent)) * math.Pow(pMissing, float64(nMissing)), nil
}