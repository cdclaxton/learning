package multihypothesis

import (
	"fmt"
	"math/rand"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestProbabilityValid(t *testing.T) {
	testCases := []struct {
		p        float64
		expected error
	}{
		{
			p:        -1.0,
			expected: ErrInvalidProbability,
		},
		{
			p:        1.1,
			expected: ErrInvalidProbability,
		},
		{
			p:        0.2,
			expected: nil,
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := probabilityValid(testCase.p)
			assert.ErrorIs(t, actual, testCase.expected)
		})
	}
}

func TestDiscreteDistributionValidate(t *testing.T) {
	testCases := []struct {
		description string
		dist        DiscreteDistribution
		expected    error
	}{
		{
			description: "empty distribution",
			dist:        DiscreteDistribution{},
			expected:    ErrDistributionIsEmpty,
		},
		{
			description: "one entry, value < 0",
			dist:        DiscreteDistribution{0: -0.1},
			expected:    ErrDistributionInvalidProb,
		},
		{
			description: "one entry, value > 1",
			dist:        DiscreteDistribution{0: 1.1},
			expected:    ErrDistributionInvalidProb,
		},
		{
			description: "one entry, valid",
			dist:        DiscreteDistribution{0: 1.0},
			expected:    nil,
		},
		{
			description: "two entries, valid",
			dist:        DiscreteDistribution{0: 0.2, 1: 0.8},
			expected:    nil,
		},
		{
			description: "two entries, invalid",
			dist:        DiscreteDistribution{0: 0.2, 1: 0.9},
			expected:    ErrDistributionDoesNotSumTo1,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual := testCase.dist.Validate()
			assert.ErrorIs(t, actual, testCase.expected)
		})
	}
}

func TestDiscreteDistributionEquals(t *testing.T) {
	testCases := []struct {
		description string
		d1          DiscreteDistribution
		d2          DiscreteDistribution
		expected    bool
	}{
		{
			description: "both distribution empty",
			d1:          DiscreteDistribution{},
			d2:          DiscreteDistribution{},
			expected:    true,
		},
		{
			description: "one entry, same",
			d1:          DiscreteDistribution{0: 1.0},
			d2:          DiscreteDistribution{0: 1.0},
			expected:    true,
		},
		{
			description: "one entry, different",
			d1:          DiscreteDistribution{0: 1.0},
			d2:          DiscreteDistribution{2: 1.0},
			expected:    false,
		},
		{
			description: "two entries, same",
			d1:          DiscreteDistribution{0: 0.2, 2: 0.8},
			d2:          DiscreteDistribution{0: 0.2, 2: 0.8},
			expected:    true,
		},
		{
			description: "two entries, different",
			d1:          DiscreteDistribution{0: 0.2, 2: 0.8},
			d2:          DiscreteDistribution{0: 0.3, 2: 0.7},
			expected:    false,
		},
		{
			description: "two entries, different lengths",
			d1:          DiscreteDistribution{0: 0.2, 2: 0.8},
			d2:          DiscreteDistribution{0: 1.0},
			expected:    false,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual := testCase.d1.Equals(testCase.d2)
			assert.Equal(t, actual, testCase.expected)
		})
	}
}

func TestVariablesSame(t *testing.T) {
	testCases := []struct {
		description   string
		expected      []string
		actual        []string
		expectedError error
	}{
		{
			description:   "empty variables",
			expected:      []string{},
			actual:        []string{},
			expectedError: nil,
		},
		{
			description:   "differing lengths",
			expected:      []string{"A"},
			actual:        []string{"A", "B"},
			expectedError: ErrIncorrectNumVariables,
		},
		{
			description:   "one variable, matching",
			expected:      []string{"A"},
			actual:        []string{"A"},
			expectedError: nil,
		},
		{
			description:   "two variables, matching",
			expected:      []string{"A", "B"},
			actual:        []string{"B", "A"},
			expectedError: nil,
		},
		{
			description:   "two variables, not matching",
			expected:      []string{"A", "B"},
			actual:        []string{"B", "C"},
			expectedError: ErrIncorrectVariableName,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual := variablesSame(testCase.expected, testCase.actual)
			assert.ErrorIs(t, actual, testCase.expectedError)
		})
	}
}

func TestHypothesisValidate(t *testing.T) {

	validName := "Hypothesis A"

	configA := map[string]bool{
		"A": true,
	}
	configAB := map[string]bool{
		"A": true,
		"B": false,
	}

	expectedVariablesA := []string{"A"}
	expectedVariablesAB := []string{"A", "B"}

	validPriorProbability := rand.Float64()
	invalidPriorProbability := 1.01 + rand.Float64()

	validDistribution := DiscreteDistribution{0: 0.1, 1: 0.7, 2: 0.2}
	invalidDistribtion := DiscreteDistribution{0: 0.1, 1: 0.7, 2: 0.3}

	testCases := []struct {
		description       string
		hypothesis        Hypothesis
		expectedVariables []string
		expected          error
	}{
		{
			description: "blank hypothesis name",
			hypothesis: Hypothesis{
				Name:             "",
				SituationConfig:  configA,
				PriorProbability: validPriorProbability,
				Distribution:     validDistribution,
			},
			expectedVariables: expectedVariablesA,
			expected:          ErrHypthesisNameIsBlank,
		},
		{
			description: "invalid prior probability",
			hypothesis: Hypothesis{
				Name:             validName,
				SituationConfig:  configA,
				PriorProbability: invalidPriorProbability,
				Distribution:     validDistribution,
			},
			expectedVariables: expectedVariablesA,
			expected:          ErrInvalidPrior,
		},
		{
			description: "missing variable",
			hypothesis: Hypothesis{
				Name:             validName,
				SituationConfig:  configA,
				PriorProbability: validPriorProbability,
				Distribution:     validDistribution,
			},
			expectedVariables: expectedVariablesAB,
			expected:          ErrIncorrectVariablesInHypothesis,
		},
		{
			description: "extra variable",
			hypothesis: Hypothesis{
				Name:             validName,
				SituationConfig:  configAB,
				PriorProbability: validPriorProbability,
				Distribution:     validDistribution,
			},
			expectedVariables: expectedVariablesA,
			expected:          ErrIncorrectVariablesInHypothesis,
		},
		{
			description: "invalid distribution",
			hypothesis: Hypothesis{
				Name:             validName,
				SituationConfig:  configA,
				PriorProbability: validPriorProbability,
				Distribution:     invalidDistribtion,
			},
			expectedVariables: expectedVariablesA,
			expected:          ErrDistributionDoesNotSumTo1,
		},
		{
			description: "valid hypothesis",
			hypothesis: Hypothesis{
				Name:             validName,
				SituationConfig:  configAB,
				PriorProbability: validPriorProbability,
				Distribution:     validDistribution,
			},
			expectedVariables: expectedVariablesAB,
			expected:          nil,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual := testCase.hypothesis.Validate(testCase.expectedVariables)
			assert.ErrorIs(t, actual, testCase.expected)
		})
	}
}

func TestEvaluateHypothesis(t *testing.T) {
	hypothesisName := "name"
	distribution := DiscreteDistribution{0: 1.0}

	testCases := []struct {
		description        string
		hypothesis         Hypothesis
		variableNameToProb map[string]float64
		expected           float64
		expectedError      error
	}{
		{
			description: "one input, true",
			hypothesis: Hypothesis{
				Name:             hypothesisName,
				SituationConfig:  map[string]bool{"A": true},
				PriorProbability: 0.8,
				Distribution:     distribution,
			},
			variableNameToProb: map[string]float64{"A": 0.9},
			expected:           0.8 * 0.9,
			expectedError:      nil,
		},
		{
			description: "one input, false",
			hypothesis: Hypothesis{
				Name:             hypothesisName,
				SituationConfig:  map[string]bool{"A": false},
				PriorProbability: 0.8,
				Distribution:     distribution,
			},
			variableNameToProb: map[string]float64{"A": 0.9},
			expected:           0.8 * (1 - 0.9),
			expectedError:      nil,
		},
		{
			description: "two inputs, one true, one false",
			hypothesis: Hypothesis{
				Name:             hypothesisName,
				SituationConfig:  map[string]bool{"A": true, "B": false},
				PriorProbability: 0.8,
				Distribution:     distribution,
			},
			variableNameToProb: map[string]float64{"A": 0.9, "B": 0.2},
			expected:           0.8 * 0.9 * (1 - 0.2),
			expectedError:      nil,
		},
		{
			description: "two inputs, both true",
			hypothesis: Hypothesis{
				Name:             hypothesisName,
				SituationConfig:  map[string]bool{"A": true, "B": true},
				PriorProbability: 0.8,
				Distribution:     distribution,
			},
			variableNameToProb: map[string]float64{"A": 0.9, "B": 0.2},
			expected:           0.8 * 0.9 * 0.2,
			expectedError:      nil,
		},
		{
			description: "two inputs, both false",
			hypothesis: Hypothesis{
				Name:             hypothesisName,
				SituationConfig:  map[string]bool{"A": false, "B": false},
				PriorProbability: 0.8,
				Distribution:     distribution,
			},
			variableNameToProb: map[string]float64{"A": 0.9, "B": 0.2},
			expected:           0.8 * (1 - 0.9) * (1 - 0.2),
			expectedError:      nil,
		},
		{
			description: "two inputs, one is missing",
			hypothesis: Hypothesis{
				Name:             hypothesisName,
				SituationConfig:  map[string]bool{"A": false, "B": false},
				PriorProbability: 0.8,
				Distribution:     distribution,
			},
			variableNameToProb: map[string]float64{"A": 0.9},
			expected:           0.0,
			expectedError:      ErrVariableNameMissing,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual, err := testCase.hypothesis.Evaluate(testCase.variableNameToProb)
			assert.ErrorIs(t, err, testCase.expectedError)
			assert.InDelta(t, testCase.expected, actual, 1e-6)
		})
	}
}

func TestValidateHypotheses(t *testing.T) {
	testCases := []struct {
		description string
		hypotheses  Hypotheses
		expected    error
	}{
		{
			description: "no hypotheses",
			hypotheses:  Hypotheses{},
			expected:    ErrNoHypotheses,
		},
		{
			description: "one hypothesis, valid",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true},
						PriorProbability: 1.0,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
				},
			},
			expected: nil,
		},
		{
			description: "one hypothesis, prob sums to less than 1",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true},
						PriorProbability: 0.9,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
				},
			},
			expected: ErrHypothesesPriorsDoNotSumTo1,
		},
		{
			description: "two hypotheses, valid",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true},
						PriorProbability: 0.2,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
					{
						Name:             "h2",
						SituationConfig:  map[string]bool{"A": false},
						PriorProbability: 0.8,
						Distribution:     DiscreteDistribution{1: 1.0},
					},
				},
			},
			expected: nil,
		},
		{
			description: "two hypotheses, priors don't sum to 1",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true},
						PriorProbability: 0.9,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
					{
						Name:             "h2",
						SituationConfig:  map[string]bool{"A": false},
						PriorProbability: 0.8,
						Distribution:     DiscreteDistribution{1: 1.0},
					},
				},
			},
			expected: ErrHypothesesPriorsDoNotSumTo1,
		},
		{
			description: "two hypotheses, inconsistent variable names",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"B": true},
						PriorProbability: 0.9,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
					{
						Name:             "h2",
						SituationConfig:  map[string]bool{"A": false},
						PriorProbability: 0.1,
						Distribution:     DiscreteDistribution{1: 1.0},
					},
				},
			},
			expected: ErrInconsistentVariablesInHypotheses,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual := testCase.hypotheses.Validate()
			assert.ErrorIs(t, actual, testCase.expected)
		})
	}
}

func TestMixtureModel(t *testing.T) {
	testCases := []struct {
		description   string
		dists         []MixtureModelComponent
		expected      DiscreteDistribution
		expectedError error
	}{
		{
			description: "one input",
			dists: []MixtureModelComponent{
				{
					Probability:  1.0,
					Distribution: DiscreteDistribution{0: 1.0},
				},
			},
			expected:      DiscreteDistribution{0: 1.0},
			expectedError: nil,
		},
		{
			description: "two inputs, priors don't sum to 1",
			dists: []MixtureModelComponent{
				{
					Probability:  0.6,
					Distribution: DiscreteDistribution{0: 1.0},
				},
				{
					Probability:  0.7,
					Distribution: DiscreteDistribution{0: 1.0},
				},
			},
			expected:      nil,
			expectedError: ErrMixtureModelProbsDoesNotSumTo1,
		},
		{
			description: "two inputs, all mass on one value",
			dists: []MixtureModelComponent{
				{
					Probability:  0.3,
					Distribution: DiscreteDistribution{2: 1.0},
				},
				{
					Probability:  0.7,
					Distribution: DiscreteDistribution{4: 1.0},
				},
			},
			expected: DiscreteDistribution{
				2: 0.3,
				4: 0.7,
			},
			expectedError: nil,
		},
		{
			description: "two inputs",
			dists: []MixtureModelComponent{
				{
					Probability:  0.3,
					Distribution: DiscreteDistribution{2: 0.8, 3: 0.2},
				},
				{
					Probability:  0.7,
					Distribution: DiscreteDistribution{2: 0.7, 4: 0.3},
				},
			},
			expected: DiscreteDistribution{
				2: 0.3*0.8 + 0.7*0.7,
				3: 0.3 * 0.2,
				4: 0.7 * 0.3,
			},
			expectedError: nil,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual, err := mixtureModel(testCase.dists)
			assert.ErrorIs(t, err, testCase.expectedError)
			assert.True(t, testCase.expected.Equals(actual))
		})
	}
}

func TestPosteriorProbOfHypotheses(t *testing.T) {
	testCases := []struct {
		description           string
		hypotheses            Hypotheses
		variableToProbability map[string]float64
		expected              []float64
	}{
		{
			description: "one hypothesis",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true},
						PriorProbability: 1.0,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
				},
			},
			variableToProbability: map[string]float64{"A": 0.2},
			expected:              []float64{1.0},
		},
		{
			description: "two hypotheses",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true},
						PriorProbability: 0.6,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
					{
						Name:             "h2",
						SituationConfig:  map[string]bool{"A": false},
						PriorProbability: 0.4,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
				},
			},
			variableToProbability: map[string]float64{"A": 0.2},
			expected: []float64{
				0.6 * 0.2 / (0.6*0.2 + 0.4*(1-0.2)),
				0.4 * (1 - 0.2) / (0.6*0.2 + 0.4*(1-0.2)),
			},
		},
		{
			description: "two hypotheses, two variables",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true, "B": true},
						PriorProbability: 0.6,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
					{
						Name:             "h2",
						SituationConfig:  map[string]bool{"A": false, "B": true},
						PriorProbability: 0.4,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
				},
			},
			variableToProbability: map[string]float64{"A": 0.2, "B": 0.7},
			expected: []float64{
				0.6 * 0.2 * 0.7 / (0.6*0.2*0.7 + 0.4*(1-0.2)*0.7),
				0.4 * (1 - 0.2) * 0.7 / (0.6*0.2*0.7 + 0.4*(1-0.2)*0.7),
			},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual, err := testCase.hypotheses.posteriorProbOfHypotheses(testCase.variableToProbability)
			assert.NoError(t, err)
			assert.True(t, probabilitiesInDelta(testCase.expected, actual, 1e-6))
		})
	}
}

func TestEvaluateHypotheses(t *testing.T) {
	testCases := []struct {
		description           string
		hypotheses            Hypotheses
		variableToProbability map[string]float64
		expected              DiscreteDistribution
		errorExpected         error
	}{
		{
			description: "one hypothesis",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true},
						PriorProbability: 1.0,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
				},
			},
			variableToProbability: map[string]float64{"A": 0.2},
			expected:              DiscreteDistribution{0: 1.0},
			errorExpected:         nil,
		},
		{
			// p(h1) = 0.4*0.2 / (0.4*0.2 + 0.6*(1-0.2))
			// p(h2) = 0.6*(1-0.2) / (0.4*0.2 + 0.6*(1-0.2))
			description: "two hypotheses",
			hypotheses: Hypotheses{
				Hypotheses: []Hypothesis{
					{
						Name:             "h1",
						SituationConfig:  map[string]bool{"A": true},
						PriorProbability: 0.4,
						Distribution:     DiscreteDistribution{0: 1.0},
					},
					{
						Name:             "h2",
						SituationConfig:  map[string]bool{"A": false},
						PriorProbability: 0.6,
						Distribution:     DiscreteDistribution{1: 1.0},
					},
				},
			},
			variableToProbability: map[string]float64{"A": 0.2},
			expected: DiscreteDistribution{
				0: 0.4 * 0.2 / (0.4*0.2 + 0.6*(1-0.2)),
				1: 0.6 * (1 - 0.2) / (0.4*0.2 + 0.6*(1-0.2)),
			},
			errorExpected: nil,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.description, func(t *testing.T) {
			actual, err := testCase.hypotheses.Evaluate(testCase.variableToProbability)
			assert.ErrorIs(t, err, testCase.errorExpected)
			assert.True(t, testCase.expected.Equals(actual))
		})
	}
}
