package main

import (
	"fmt"
	"math"
	"strconv"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/calculator2/parser"
)

type CalcListener struct {
	*parser.BaseCalcListener
	stack []float64
}

func (c *CalcListener) push(x float64) {
	c.stack = append(c.stack, x)
}

func (c *CalcListener) pop() float64 {
	if len(c.stack) < 1 {
		panic("Stack is empty, unable to pop")
	}

	result := c.stack[len(c.stack)-1]
	c.stack = c.stack[:len(c.stack)-1]
	return result
}

func toFloat64(s string) float64 {
	value, err := strconv.ParseFloat(s, 64)
	if err != nil {
		panic(fmt.Sprintf("Unable to convert '%s' (type %T) to a float", s, s))
	}
	return value
}

func (c *CalcListener) ExitExpr(ctx *parser.ExprContext) {

	if ctx.GetOp() == nil {
		return
	}

	right := c.pop()
	left := c.pop()

	switch ctx.GetOp().GetTokenType() {
	case parser.CalcParserADD:
		c.push(right + left)
	case parser.CalcParserSUB:
		c.push(left - right)
	}
}

func (c *CalcListener) ExitTerm(ctx *parser.TermContext) {
	if ctx.GetOp() == nil {
		return
	}

	right := c.pop()
	left := c.pop()

	switch ctx.GetOp().GetTokenType() {
	case parser.CalcParserMUL:
		c.push(left * right)
	case parser.CalcParserDIV:
		c.push(left / right)
	}
}

func (c *CalcListener) ExitNumber(ctx *parser.NumberContext) {
	c.push(toFloat64(ctx.GetText()))
}

func (c *CalcListener) ExitUnaryFactor(ctx *parser.UnaryFactorContext) {
	if ctx.ADD() != nil {
		// Nothing to do
	} else if ctx.SUB() != nil {
		c.push(-c.pop())
	}
}

func (c *CalcListener) getValue() float64 {
	if len(c.stack) == 0 {
		return 0.0
	}
	return c.stack[0]
}

func calculator(expression string) float64 {

	// Create the lexer
	is := antlr.NewInputStream(expression)
	lexer := parser.NewCalcLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)

	// Create the parser
	p := parser.NewCalcParser(stream)

	// Parse the expression by walking the tree
	var listener CalcListener
	antlr.ParseTreeWalkerDefault.Walk(&listener, p.Expr())

	return listener.getValue()
}

// runCalculator and check the answer is as expected.
func runCalculator(expression string, expected float64) {
	result := calculator(expression)
	if math.Abs(result-expected) < 1e-6 {
		fmt.Printf("✓ %s = %f\n", expression, expected)
	} else {
		fmt.Printf("⨯ %s = %f ≠ %f\n", expression, result, expected)
	}
}

func main() {
	fmt.Println("Calculator")
	runCalculator("3", 3)
	runCalculator("-3", -3)
	runCalculator("+3", 3)
	runCalculator("3 + 2", 3+2)
	runCalculator("3 - 2", 3-2)
	runCalculator("3 * 2", 3*2)
	runCalculator("3 * -2", 3*-2)
	runCalculator("3 / 2", 3.0/2.0)
	runCalculator("3 + (2 * 10)", 3+(2*10))
	runCalculator("3 / (2 * 10)", 3.0/(2*10))
	runCalculator("3 + (2 * (10 - 2))", 3+(2*(10-2)))
}
