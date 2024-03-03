package main

import (
	"fmt"
	"math/rand"
	"reflect"
	"testing"
	"testing/quick"

	"github.com/stretchr/testify/assert"
)

func TestReverseSlice(t *testing.T) {
	testCases := []struct {
		data     []int
		expected []int
	}{
		{
			data:     []int{},
			expected: []int{},
		},
		{
			data:     []int{1},
			expected: []int{1},
		},
		{
			data:     []int{1, 2},
			expected: []int{2, 1},
		},
		{
			data:     []int{1, 2, 3},
			expected: []int{3, 2, 1},
		},
	}

	for idx, testCase := range testCases {
		t.Run(fmt.Sprintf("Test %d", idx), func(t *testing.T) {
			actual := ReverseSlice(testCase.data)
			assert.Equal(t, testCase.expected, actual)
		})
	}
}

func slicesEqual(s1, s2 []int) bool {
	if len(s1) != len(s2) {
		return false
	}

	for idx := range s1 {
		if s1[idx] != s2[idx] {
			return false
		}
	}

	return true
}

func TestReverseSlicePropertyBased(t *testing.T) {
	property := func(s []int) bool {
		return slicesEqual(ReverseSlice(ReverseSlice(s)), s)
	}

	assert.NoError(t, quick.Check(property, nil))
}

func TestPersonBirthday(t *testing.T) {
	property := func(p *Person) bool {
		if p == nil {
			return true
		}

		original := &Person{p.Name, p.Age}
		p.birthday()
		return p.isOlderThan(original)
	}

	// The generator will generate a nil Person and a Person with a negative age
	assert.NoError(t, quick.Check(property, nil))
}

func randomPerson(r *rand.Rand) *Person {
	return &Person{
		Name: "Bob",
		Age:  r.Intn(110),
	}
}

func TestPersonBirthday2(t *testing.T) {
	property := func(p *Person) bool {
		original := &Person{p.Name, p.Age}
		p.birthday()
		return p.isOlderThan(original)
	}

	config := quick.Config{
		MaxCount: 10,
		Values: func(v []reflect.Value, r *rand.Rand) {
			v[0] = reflect.ValueOf(randomPerson(r))
		},
	}

	assert.NoError(t, quick.Check(property, &config))
}

func TestPersonAddYears(t *testing.T) {
	property := func(p *Person, n int) bool {
		original := &Person{p.Name, p.Age}
		p.addYears(n)
		return p.isOlderThan(original)
	}

	config := quick.Config{
		MaxCount: 10,
		Values: func(v []reflect.Value, r *rand.Rand) {
			v[0] = reflect.ValueOf(randomPerson(r))
			v[1] = reflect.ValueOf(r.Intn(100))
		},
	}

	assert.NoError(t, quick.Check(property, &config))
}
