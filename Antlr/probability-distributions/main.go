package main

import (
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/probabilitydistributions/parser"
)

// Distribution represents a discrete probability distribution.
type Distribution map[int]float64

// CumulativeProbability of the distribution for value x.
func (d Distribution) CumulativeProbability(x int) float64 {
	cumProb := 0.0

	for value, prob := range d {
		if value <= x {
			cumProb += prob
		}
	}

	return cumProb
}

func (d Distribution) Format() string {
	var sb strings.Builder

	sb.WriteString("{")

	values := uniqueValues(d)
	for idx, value := range values {
		sb.WriteString(fmt.Sprintf("%d:%f", value, d[value]))
		if idx < len(values)-1 {
			sb.WriteString(", ")
		}
	}

	sb.WriteString("}")

	return sb.String()
}

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

func (i *InterpreterListener) ExitNoisyMax(ctx *parser.NoisyMaxContext) {
	right, left := i.pop(), i.pop()
	i.push(NoisyMax(right, left))
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

func main() {

	if len(os.Args) != 2 {
		fmt.Printf("Usage: %s <program file>\n", os.Args[0])
		os.Exit(1)
	}

	fmt.Println("=== Probability Distribution Calculator ===")

	// Read the program from file
	contents, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	program := string(contents)
	for idx, line := range strings.Split(program, "\n") {
		fmt.Printf("%d | %s\n", idx+1, line)
	}
	fmt.Println()

	// Run the program
	result := run(program)

	// Show the results
	variables := make([]string, 0, len(result))
	for variable := range result {
		variables = append(variables, variable)
	}
	sort.Strings(variables)

	for _, variable := range variables {
		fmt.Printf("%s: %s\n", variable, result[variable].Format())
	}
}
