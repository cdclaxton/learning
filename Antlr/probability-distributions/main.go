package main

import (
	"fmt"
	"math"
	"strconv"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/probabilitydistributions/parser"
)

// Distribution represents a discrete probability distribution.
type Distribution map[int]float64

type InterpreterListener struct {
	*parser.BaseProbabilityDistributionsListener
	memory       map[string]Distribution // Variable name to distribution
	distribution Distribution            // Used when constructing a distribution
	stack        []Distribution
}

func NewInterpreterListener() *InterpreterListener {
	return &InterpreterListener{
		memory: map[string]Distribution{},
		stack:  []Distribution{},
	}
}

// pop a distribution from the stack.
func (i *InterpreterListener) pop() Distribution {
	if len(i.stack) == 0 {
		panic("Stack is empty, cannot pop")
	}

	// Clone the distribution
	dist := Distribution{}
	for value, prob := range i.stack[len(i.stack)-1] {
		dist[value] = prob
	}

	i.stack = i.stack[:len(i.stack)-1]
	return dist
}

// push a clone of the distribution onto the stack.
func (i *InterpreterListener) push(dist Distribution) {
	i.stack = append(i.stack, Distribution{})
	for value, prob := range dist {
		i.stack[len(i.stack)-1][value] = prob
	}
}

// EnterDist prepares a space for a literal distribution.
func (i *InterpreterListener) EnterDist(ctx *parser.DistContext) {
	i.distribution = Distribution{}
}

// ExitElement retrieves the value-probability pair and adds those to the
// distribution under construction.
func (i *InterpreterListener) ExitElement(ctx *parser.ElementContext) {
	value := toInt(ctx.INT().GetText())
	probability := toFloat64(ctx.FLOAT().GetText())
	i.distribution[value] = probability
}

// ExitAssign makes pops a distribution from the stack and adds it to the
// memory.
func (i *InterpreterListener) ExitAssign(ctx *parser.AssignContext) {
	variableName := ctx.ID().GetText()
	i.memory[variableName] = i.pop()
}

// ExitExprDist pushes the distribution onto the stack.
func (i *InterpreterListener) ExitExprDist(ctx *parser.ExprDistContext) {
	i.push(i.distribution)
}

// ExitId pushes the distribution referenced by the ID to the stack.
func (i *InterpreterListener) ExitId(ctx *parser.IdContext) {
	variableName := ctx.ID().GetText()
	dist, ok := i.memory[variableName]
	if !ok {
		panic(fmt.Sprintf("Variable '%s' not defined", variableName))
	}
	i.push(dist)
}

func (i *InterpreterListener) ExitAddSub(ctx *parser.AddSubContext) {
	right, left := i.pop(), i.pop()

	switch ctx.GetOp().GetTokenType() {
	case parser.ProbabilityDistributionsParserADD:
		i.push(CombineDistributions(left, right, Add))
	case parser.ProbabilityDistributionsParserSUB:
		i.push(CombineDistributions(left, right, Sub))
	}
}

func (i *InterpreterListener) ExitMulDiv(ctx *parser.MulDivContext) {
	right, left := i.pop(), i.pop()

	switch ctx.GetOp().GetTokenType() {
	case parser.ProbabilityDistributionsLexerMUL:
		i.push(CombineDistributions(left, right, Mul))
	case parser.ProbabilityDistributionsLexerDIV:
		i.push(CombineDistributions(left, right, Div))
	}
}

// toFloat64 converts a string to a float64 value, but panics if the string
// cannot be converted.
func toFloat64(s string) float64 {
	value, err := strconv.ParseFloat(s, 64)
	if err != nil {
		panic(fmt.Sprintf("Unable to convert '%s' (type %T) to a float", s, s))
	}
	return value
}

// toInt converts a string to an int value, but panics if the string
// cannot be converted.
func toInt(s string) int {
	value, err := strconv.Atoi(s)
	if err != nil {
		panic(fmt.Sprintf("Unable to convert '%s' (type %T) to a int", s, s))
	}
	return value
}

func run(program string) map[string]Distribution {
	// Create the lexer
	is := antlr.NewInputStream(program)
	lexer := parser.NewProbabilityDistributionsLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)

	// Create the parser
	p := parser.NewProbabilityDistributionsParser(stream)

	// Parse the expression by walking the tree
	listener := NewInterpreterListener()
	antlr.ParseTreeWalkerDefault.Walk(listener, p.Prog())

	return listener.memory
}

func distributionsEqual(actual, expected Distribution, tol float64) bool {
	if len(actual) != len(expected) {
		return false
	}

	for value, actualProb := range actual {
		expectedProb, ok := expected[value]
		if !ok || math.Abs(expectedProb-actualProb) > tol {
			return false
		}
	}

	return true
}

func distributionsInTolerance(actual, expected map[string]Distribution,
	tol float64) bool {

	if len(actual) != len(expected) {
		return false
	}

	for variableName, expectedDistribution := range expected {
		actualDistribution, ok := actual[variableName]
		if !ok {
			return false
		}

		if !distributionsEqual(expectedDistribution, actualDistribution, tol) {
			return false
		}
	}

	return true
}

func calculate(program string, name string, expected map[string]Distribution) {
	result := run(program)
	if distributionsInTolerance(result, expected, 1e-6) {
		fmt.Printf("✓ Correct - %s\n", name)
	} else {
		fmt.Printf("⨯ Incorrect - %s - Expected %v, got %v\n", name, expected,
			result)
	}
}

type testCase struct {
	program        string
	description    string
	expectedMemory map[string]Distribution
}

func main() {
	fmt.Println("=== Probability Distribution Calculator ===")

	testCases := []testCase{
		{
			program:     "a = {1:1.0}\n",
			description: "Single distribution, one element",
			expectedMemory: map[string]Distribution{
				"a": {1: 1.0},
			},
		},
		{
			program:     "a = {1:0.8, 2:0.2}\n",
			description: "Single distribution, two elements",
			expectedMemory: map[string]Distribution{
				"a": {1: 0.8, 2: 0.2},
			},
		},
		{
			program:     "a = {1:1.0}\nb = a\n",
			description: "Copy a distribution",
			expectedMemory: map[string]Distribution{
				"a": {1: 1.0},
				"b": {1: 1.0},
			},
		},
		{
			program:     "a = {1:1.0}\na = {2:1.0}\n",
			description: "Redefine a distribution",
			expectedMemory: map[string]Distribution{
				"a": {2: 1.0},
			},
		},
		{
			program:     "a = {1:1.0}\nb = {3:1.0}\nc = a + b\n",
			description: "Add two distributions",
			expectedMemory: map[string]Distribution{
				"a": {1: 1.0},
				"b": {3: 1.0},
				"c": {4: 1.0},
			},
		},
		{
			program:     "a = {5:0.2, 6:0.8}\nb = {3:1.0}\nc = a - b\n",
			description: "Subtract two distributions",
			expectedMemory: map[string]Distribution{
				"a": {5: 0.2, 6: 0.8},
				"b": {3: 1.0},
				"c": {2: 0.2, 3: 0.8},
			},
		},
		{
			program:     "a = {5:0.2, 6:0.8}\nb = {3:1.0}\nc = a * b\n",
			description: "Multiply two distributions",
			expectedMemory: map[string]Distribution{
				"a": {5: 0.2, 6: 0.8},
				"b": {3: 1.0},
				"c": {15: 0.2, 18: 0.8},
			},
		},
		{
			program:     "a = {10:0.2, 6:0.8}\nb = {2:1.0}\nc = a / b\n",
			description: "Divide two distributions",
			expectedMemory: map[string]Distribution{
				"a": {10: 0.2, 6: 0.8},
				"b": {2: 1.0},
				"c": {5: 0.2, 3: 0.8},
			},
		},
	}

	for _, testCase := range testCases {
		calculate(testCase.program, testCase.description,
			testCase.expectedMemory)
	}
}
