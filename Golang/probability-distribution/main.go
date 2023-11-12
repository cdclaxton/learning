package main

import (
	"errors"
	"fmt"
	"math"
)

// Discrete probability distribution with a sparse representation
type DiscreteDistribution map[float64]float64

const Tolerance = 1e-8

func (d DiscreteDistribution) Equal(d2 DiscreteDistribution) bool {
	if d == nil && d2 != nil {
		return false
	} else if d != nil && d2 == nil {
		return false
	} else if d == nil && d2 == nil {
		return true
	}

	if len(d) != len(d2) {
		return false
	}

	for value, prob := range d {
		prob2, ok := d2[value]
		if !ok {
			fmt.Printf("value %f is missing", value)
			return false
		}

		if math.Abs(prob - prob2) > Tolerance {
			fmt.Printf("expected %f, got %f", prob, prob2)			
			return false
		}
	}

	return true
}

var (
	ErrNilDistribution = errors.New("distribution is nil")
	ErrEmptyDistribution = errors.New("empty probability distribution")
	ErrInvalidMaxError = errors.New("invalid maximum error")
	ErrTotalOutsidePermittedRange = errors.New("total probability outside of permitted range")
	ErrValueOutsidePermittedRange = errors.New("probability outside permitted range")
)

// totalProbability of the distribution.
func totalProbability(dist DiscreteDistribution) float64 {
	total := 0.0
	for _, prob := range dist {
		total += math.Abs(prob)
	}
	return total
}

// correctDistribution if it is within tolerance.
func correctDistribution(dist DiscreteDistribution, maxError float64) (DiscreteDistribution, error) {

	if dist == nil {
		return nil, ErrNilDistribution
	}

	if len(dist) == 0 {
		return nil, ErrEmptyDistribution
	}

	if maxError < 0 {
		return nil, ErrInvalidMaxError
	}

	// Calculate the total probability
	total := totalProbability(dist)
	if math.Abs(total - 1.0) > (maxError * float64(len(dist))) {
		return nil, fmt.Errorf("%w: %f", ErrTotalOutsidePermittedRange, total)
	}

	// Normalise each value
	distCorrected := make(DiscreteDistribution, len(dist))
	for value, prob := range dist {
		if prob < -maxError || prob > (1.0 + maxError) {
			return nil, ErrValueOutsidePermittedRange
		}

		distCorrected[value] = math.Abs(prob) / total
	}

	// Check the total of the normalised distribution
	total = totalProbability(distCorrected)
	if math.Abs(total - 1.0) > (maxError * float64(len(dist))) {
		return nil, fmt.Errorf("%w: %f", ErrTotalOutsidePermittedRange, total)
	}

	return distCorrected, nil
}