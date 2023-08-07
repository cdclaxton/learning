package multihypothesis

import (
	"errors"
	"fmt"
	"math"
	"sort"

	"golang.org/x/exp/maps"
)

var (
	ErrHypthesisNameIsBlank              = errors.New("hypothesis name is blank")
	ErrNoHypotheses                      = errors.New("no hypotheses")
	ErrInputNameMappingEmpty             = errors.New("input name to variable mapping is empty")
	ErrBlankVariableName                 = errors.New("variable name is blank")
	ErrInvalidPrior                      = errors.New("invalid prior probability")
	ErrIncorrectNumVariables             = errors.New("incorrect number of variables")
	ErrIncorrectVariableName             = errors.New("incorrect variable name")
	ErrIncorrectVariablesInHypothesis    = errors.New("incorrect variables in hypothesis")
	ErrDistributionIsEmpty               = errors.New("distribution is empty")
	ErrDistributionInvalidProb           = errors.New("discrete distribution has an invalid probability")
	ErrInvalidProbability                = errors.New("invalid probability")
	ErrDistributionDoesNotSumTo1         = errors.New("distribution does not sum to 1")
	ErrMixtureModelProbsDoesNotSumTo1    = errors.New("inputs to mixture model do not sum to 1")
	ErrOutputOfMixtureModelIsInvalid     = errors.New("output of mixture model is invalid")
	ErrVariableNameMissing               = errors.New("variable name is missing")
	ErrInconsistentVariablesInHypotheses = errors.New("inconsistent variables in hypotheses")
	ErrHypothesesPriorsDoNotSumTo1       = errors.New("hypotheses priors do not sum to 1")
)

const (
	tolerance = 1e-6
)

// DiscreteDistribution represents a probability mass function (PMF).
type DiscreteDistribution map[int]float64

// Validate a discrete probability distribution.
func (d DiscreteDistribution) Validate() error {
	if len(d) == 0 {
		return ErrDistributionIsEmpty
	}

	total := 0.0
	for _, p := range d {
		if err := probabilityValid(p); err != nil {
			return ErrDistributionInvalidProb
		}
		total += p
	}

	if math.Abs(total-1.0) > tolerance {
		return ErrDistributionDoesNotSumTo1
	}

	return nil
}

// Equals returns true if two discrete distributions are within tolerance.
func (d DiscreteDistribution) Equals(d2 DiscreteDistribution) bool {
	if len(d) != len(d2) {
		return false
	}

	for value, prob := range d {
		prob2, ok := d2[value]
		if !ok {
			return false
		}

		if math.Abs(prob-prob2) > tolerance {
			return false
		}
	}

	return true
}

// probabilityValid returns true if the value is a valid probability.
func probabilityValid(p float64) error {
	if p < 0.0 || p > 1.0 {
		return ErrInvalidProbability
	}

	return nil
}

// Hypothesis represents a configuration of input variables.
type Hypothesis struct {
	Name             string // Used if there is an issue with the hypothesis to help the user
	SituationConfig  map[string]bool
	PriorProbability float64
	Distribution     DiscreteDistribution
}

// variables used in the hypothesis.
func (h Hypothesis) variables() []string {
	return maps.Keys(h.SituationConfig)
}

// variablesSame returns an error if the expected variables differ from the
// actual variables present in a hypothesis.
func variablesSame(expected []string, actual []string) error {

	// Check the lengths are the same
	if len(expected) != len(actual) {
		return fmt.Errorf("%w: expected=%v, actual=%v",
			ErrIncorrectNumVariables, expected, actual)
	}

	// Sort the variables
	sort.Strings(expected)
	sort.Strings(actual)

	for i := range expected {
		if expected[i] != actual[i] {
			return fmt.Errorf("%w: expected=%v, actual=%v",
				ErrIncorrectVariableName, expected, actual)
		}
	}

	return nil
}

// Validate the hypothesis.
func (h Hypothesis) Validate(expectedVariables []string) error {

	if len(h.Name) == 0 {
		return ErrHypthesisNameIsBlank
	}

	// Check the prior probability is valid
	if probabilityValid(h.PriorProbability) != nil {
		return fmt.Errorf("%w: %f", ErrInvalidPrior, h.PriorProbability)
	}

	// Check the required variables are present in the hypothesis
	if err := variablesSame(expectedVariables, h.variables()); err != nil {
		return fmt.Errorf("%w: %w", ErrIncorrectVariablesInHypothesis, err)
	}

	// Check the discrete distribution is valid
	return h.Distribution.Validate()
}

// Evaluate the hypothesis to return the unnormalised probability.
// This function returns p(hypothesis) * prod_{i} p(i) where i denotes an
// input and p(i) is the input's probability.
func (h Hypothesis) Evaluate(variableNameToProb map[string]float64) (float64, error) {

	total := math.Log(h.PriorProbability)
	for variableName, ongoing := range h.SituationConfig {
		prob, ok := variableNameToProb[variableName]
		if !ok {
			return 0.0, fmt.Errorf("%w: %s", ErrVariableNameMissing, variableName)
		}

		if ongoing {
			total += math.Log(prob)
		} else {
			total += math.Log(1.0 - prob)
		}
	}

	return math.Exp(total), nil
}

type Hypotheses struct {
	Hypotheses []Hypothesis // Multiple hypotheses
}

// Validate the hypotheses.
func (h *Hypotheses) Validate() error {

	if len(h.Hypotheses) == 0 {
		return ErrNoHypotheses
	}

	// Get the expected variable names from the first hypothesis
	variableNames := h.Hypotheses[0].variables()

	// Validate each hypothesis
	totalPrior := 0.0
	for _, hypothesis := range h.Hypotheses {
		if err := hypothesis.Validate(variableNames); err != nil {
			return fmt.Errorf("%w: %w", ErrInconsistentVariablesInHypotheses, err)
		}

		totalPrior += hypothesis.PriorProbability
	}

	// Check the prior probabilities sum to 1
	if math.Abs(totalPrior-1.0) > tolerance {
		return ErrHypothesesPriorsDoNotSumTo1
	}

	return nil
}

// probabilitiesInDelta returns true if the expected and actual probabilities
// are within a given tolerance (delta).
func probabilitiesInDelta(expected []float64, actual []float64, delta float64) bool {
	if len(expected) != len(actual) {
		return false
	}

	for idx := range expected {
		// Check the probabilities at position idx are valid
		if err := probabilityValid(expected[idx]); err != nil {
			return false
		}

		if err := probabilityValid(actual[idx]); err != nil {
			return false
		}

		// Check the differences are within tolerance
		if math.Abs(expected[idx]-actual[idx]) > delta {
			return false
		}
	}

	return true
}

// posteriorProbOfHypotheses calculates p(H_i|S=1).
func (h *Hypotheses) posteriorProbOfHypotheses(variableToProbability map[string]float64) ([]float64, error) {

	probs := make([]float64, len(h.Hypotheses))
	totalProb := 0.0
	var err error

	// Calculate the unnormalised probability of each hypothesis
	for idx, hypothesis := range h.Hypotheses {
		probs[idx], err = hypothesis.Evaluate(variableToProbability)
		if err != nil {
			return nil, err
		}

		totalProb += probs[idx]
	}

	// Normalise the probability of each hypothesis
	for idx := range probs {
		probs[idx] = probs[idx] / totalProb
	}

	return probs, nil
}

// Evaluate hypotheses to return a single probability distribution.
func (h *Hypotheses) Evaluate(variableToProbability map[string]float64) (DiscreteDistribution, error) {

	// Calculate the probability of each hypothesis
	probs, err := h.posteriorProbOfHypotheses(variableToProbability)
	if err != nil {
		return nil, err
	}

	// Gather the distributions and their probabilities for the mixture model
	dists := make([]MixtureModelComponent, len(h.Hypotheses))
	for idx := range h.Hypotheses {
		dists[idx] = MixtureModelComponent{
			Probability:  probs[idx],
			Distribution: h.Hypotheses[idx].Distribution,
		}
	}

	// Calculate the output discrete probability distribution
	return mixtureModel(dists)
}

// MixtureModelComponent represents a component of a mixture model.
type MixtureModelComponent struct {
	Probability  float64
	Distribution DiscreteDistribution
}

func (m MixtureModelComponent) String() string {
	return fmt.Sprintf("MixtureModelComponent(p=%f, dist=%v)", m.Probability, m.Distribution)
}

// mixtureModel given the list of components.
func mixtureModel(dists []MixtureModelComponent) (DiscreteDistribution, error) {

	result := DiscreteDistribution{}
	probsTotal := 0.0

	for _, dist := range dists {
		probsTotal += dist.Probability

		for value, prob := range dist.Distribution {
			_, ok := result[value]
			if !ok {
				// Value hasn't been seen before
				result[value] = dist.Probability * prob
			} else {
				result[value] += dist.Probability * prob
			}
		}
	}

	// Check that the input probabilities sum to 1
	if math.Abs(probsTotal-1.0) > tolerance {
		return nil, ErrMixtureModelProbsDoesNotSumTo1
	}

	// Ensure the output probability distribution is valid
	if err := result.Validate(); err != nil {
		return nil, ErrOutputOfMixtureModelIsInvalid
	}

	return result, nil
}
