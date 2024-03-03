package main

import (
	"math/rand"
	"reflect"
	"testing"
	"testing/quick"

	"github.com/stretchr/testify/assert"
	"pgregory.net/rapid"
)

// Example failure #2: failed on input 111, 96
func TestBrokenAddQuick(t *testing.T) {
	property := func(a, b int) bool {
		return brokenAdd(a, b) > a && brokenAdd(a, b) > b
	}

	config := quick.Config{
		MaxCount: 1000,
		Values: func(v []reflect.Value, r *rand.Rand) {
			v[0] = reflect.ValueOf(1 + r.Intn(120))
			v[1] = reflect.ValueOf(1 + r.Intn(120))
		},
	}

	assert.NoError(t, quick.Check(property, &config))
}

// Example of a failed test
// [rapid] draw a: 101
// [rapid] draw b: 2
func TestBrokenAddRapid(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		a := rapid.IntRange(1, 120).Draw(t, "a")
		b := rapid.IntRange(1, 120).Draw(t, "b")
		result := brokenAdd(a, b)
		assert.True(t, result > a && result > b)
	})
}
