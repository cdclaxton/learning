package main

import (
	"cmp"
	"strings"

	"golang.org/x/exp/constraints"
)

func simpleMax[T cmp.Ordered](values []T) T {
	if len(values) == 0 {
		panic("no values")
	}

	maxValue := values[0]
	for i := 1; i < len(values); i++ {
		if values[i] > maxValue {
			maxValue = values[i]
		}
	}

	return maxValue
}

type Number interface {
	constraints.Float | constraints.Integer
}

func mean[T Number](values []T) float64 {
	total := 0.0
	for _, v := range values {
		total += float64(v)
	}

	return total / float64(len(values))
}

// -----------------------------------------------------------------------------
// Example using a custom interface
// -----------------------------------------------------------------------------

type Action string

type HasAction interface {
	GetAction() Action
}

type Message struct {
	Id     string
	Action Action
}

func NewMessage(id string, action string) Message {
	return Message{
		Id:     id,
		Action: Action(action),
	}
}

func (m Message) GetAction() Action {
	return m.Action
}

func getAction[T HasAction](obj T) Action {
	return obj.GetAction()
}

// -----------------------------------------------------------------------------
// Example using the ~ operator
// -----------------------------------------------------------------------------

func upperCase[T ~string](text T) string {
	return strings.ToUpper(string(text))
}
