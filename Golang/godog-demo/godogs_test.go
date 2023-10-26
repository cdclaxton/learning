package main

import (
	"context"
	"errors"
	"fmt"
	"testing"

	"github.com/cucumber/godog"
)

// godogsCtxKey is the key for the number of godogs in context.Context
type godogsCtxKey struct{}

func thereAreGodogs(ctx context.Context, available int) (context.Context, error) {
	return context.WithValue(ctx, godogsCtxKey{}, available), nil
}

func iEat(ctx context.Context, num int) (context.Context, error) {
	
	available, ok := ctx.Value(godogsCtxKey{}).(int)
	if !ok {
		return ctx, errors.New("there are no godogs available")
	}

	if available < num {
		return ctx, fmt.Errorf("you cannot eat %d godogs, there are %d available", num, available)
	}

	available -= num

	return context.WithValue(ctx, godogsCtxKey{}, available), nil
}



func thereShouldBeRemaining(ctx context.Context, remaining int) error {

	available, ok := ctx.Value(godogsCtxKey{}).(int)
	if !ok {
		return errors.New("there are no godogs available")
	}

	if available != remaining {
		return fmt.Errorf("expected %d godogs remaining, but there is %d", remaining, available)
	}

	return nil
}

func TestFeatures(t *testing.T) {
	suite := godog.TestSuite{
		ScenarioInitializer: InitialiseScenario,
		Options: &godog.Options{
			Format: "pretty",
			Paths: []string{"features/godogs.feature"},
			TestingT: t,
		},
	}

	if suite.Run() != 0 {
		t.Fatal("non-zero status returned, failed to run feature tests")
	}
}

func InitialiseScenario(sc *godog.ScenarioContext) {
	sc.Given(`^there are (\d+) godogs$`, thereAreGodogs)
	sc.When(`^I eat (\d+)$`, iEat)
	sc.Then(`^there should be (\d+) remaining`, thereShouldBeRemaining)
}

