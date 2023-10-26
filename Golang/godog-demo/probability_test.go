package main

import (
	"context"
	"errors"
	"fmt"
	"math"
	"testing"

	"github.com/cucumber/godog"
)

// Keys in the context struct
type nTokensPresent struct{}
type nTokensMissing struct{}
type pMissing struct{}
type occProbability struct{}

func thereAreTokensPresent(ctx context.Context, numPresent int) (context.Context, error) {
	if numPresent < 0 {
		return ctx, fmt.Errorf("invalid number of tokens present: %d", numPresent)
	}

	return context.WithValue(ctx, nTokensPresent{}, numPresent), nil
}

func thereAreTokensMissing(ctx context.Context, numMissing int) (context.Context, error) {
	if numMissing < 0 {
		return ctx, fmt.Errorf("invalid number of tokens missing: %d", numMissing)
	}	

	return context.WithValue(ctx, nTokensMissing{}, numMissing), nil
}

func probMissing(ctx context.Context, prob float64) (context.Context, error) {
	if prob < 0.0 || prob > 1.0 {
		return ctx, fmt.Errorf("invalid probability: %f", prob)
	}

	return context.WithValue(ctx, pMissing{}, prob), nil
}

func calcProbability(ctx context.Context) (context.Context, error) {

	nPresent, ok := ctx.Value(nTokensPresent{}).(int)
	if !ok {
		return ctx, errors.New("number of tokens present not defined")
	}

	nMissing, ok := ctx.Value(nTokensMissing{}).(int)
	if !ok {
		return ctx, errors.New("number of tokens missing not defined")
	}

	prob, ok := ctx.Value(pMissing{}).(float64)
	if !ok {
		return ctx, errors.New("probability of a missing token not defined")
	}

	prob, err := occurrenceProbability(nPresent, nMissing, prob)
	if err != nil {
		return ctx, err
	}

	return context.WithValue(ctx, occProbability{}, prob), nil
}

func probShouldBe(ctx context.Context, expected float64) (context.Context, error) {
	actualProb, ok := ctx.Value(occProbability{}).(float64)
	if !ok {
		return ctx, errors.New("actual probability not calculated")
	}

	if math.Abs(expected - actualProb) > 1e-6 {
		return ctx, fmt.Errorf("expected %f, got %f", expected, actualProb)
	}

	return ctx, nil
}

func TestProbabilityFeatures(t *testing.T) {
	suite := godog.TestSuite{
		ScenarioInitializer: InitialiseProbabilityScenario,
		Options: &godog.Options{
			Format: "pretty",
			Paths: []string{"features/probability.feature"},
			TestingT: t,
		},
	}

	if suite.Run() != 0 {
		t.Fatal("non-zero status returned, failed to run feature tests")
	}
}


func InitialiseProbabilityScenario(sc *godog.ScenarioContext) {
	sc.Step(`^there are (\d+) tokens present`, thereAreTokensPresent)
	sc.Step(`^there are (\d+) tokens missing`, thereAreTokensMissing)
	sc.Step(`^the probability of a missing token is ([0-9]*\.?[0-9]*)`, probMissing)
	sc.Step(`^I calculate the probability`, calcProbability)
	sc.Step(`^the occurrence probability should be ([0-9]*\.?[0-9]*)`, probShouldBe)
}