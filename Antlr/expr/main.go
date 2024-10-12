package main

import (
	"fmt"
	"reflect"
	"strconv"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/expr/parser"
)

type ExprListener struct {
	*parser.BaseExprListener
	memory map[string]int // map of variable name to value
	stack  []int
}

func NewExprListener() *ExprListener {
	return &ExprListener{
		memory: map[string]int{},
		stack:  []int{},
	}
}

func (c *ExprListener) push(x int) {
	c.stack = append(c.stack, x)
}

func (c *ExprListener) pop() int {
	if len(c.stack) < 1 {
		panic("Stack is empty, unable to pop")
	}

	result := c.stack[len(c.stack)-1]
	c.stack = c.stack[:len(c.stack)-1]
	return result
}

func toInt(s string) int {
	value, err := strconv.Atoi(s)
	if err != nil {
		panic(fmt.Sprintf("Unable to convert '%s' (type %T) to a int", s, s))
	}
	return value
}

func (c *ExprListener) ExitAssign(ctx *parser.AssignContext) {
	variableName := ctx.ID().GetText()
	value := c.pop()
	c.memory[variableName] = value
}

func (c *ExprListener) ExitInt(ctx *parser.IntContext) {
	v := toInt(ctx.INT().GetText())
	c.push(v)
}

func (c *ExprListener) ExitId(ctx *parser.IdContext) {
	variable := ctx.ID().GetText()
	value, ok := c.memory[variable]
	if !ok {
		panic(fmt.Sprintf("Variable '%s' doesn't exist", variable))
	}
	c.push(value)
}

func (c *ExprListener) ExitAddSub(ctx *parser.AddSubContext) {
	right, left := c.pop(), c.pop()

	switch ctx.GetOp().GetTokenType() {
	case parser.ExprParserADD:
		c.push(left + right)
	case parser.ExprParserSUB:
		c.push(left - right)
	}
}

func (c *ExprListener) ExitMulDiv(ctx *parser.MulDivContext) {
	right, left := c.pop(), c.pop()

	switch ctx.GetOp().GetTokenType() {
	case parser.ExprParserMUL:
		c.push(left * right)
	case parser.ExprParserDIV:
		c.push(left / right)
	}
}

func intepreter(expression string) map[string]int {

	// Create the lexer
	is := antlr.NewInputStream(expression)
	lexer := parser.NewExprLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)

	// Create the parser
	p := parser.NewExprParser(stream)

	// Parse the expression by walking the tree
	listener := NewExprListener()
	antlr.ParseTreeWalkerDefault.Walk(listener, p.Prog())

	return listener.memory
}

// run and check the interpreter's memory is as expected.
func run(expression string, name string, expected map[string]int) {
	result := intepreter(expression)
	correct := reflect.DeepEqual(result, expected)
	if !correct {
		fmt.Printf("Incorrect - %s - Expected %v, got %v\n",
			name, expected, result)
	} else {
		fmt.Printf("Correct - %s\n", name)
	}
}

func main() {
	fmt.Println("=== Intepreter ===")
	run("a = 3\n", "Single assignment", map[string]int{"a": 3})
	run("a = 3\nb = 2\n", "Two assignments", map[string]int{"a": 3, "b": 2})
	run("a = 3\nb = a\n", "Variable assignments", map[string]int{"a": 3, "b": 3})
	run("a = 3 + 2\n", "Summation assignment", map[string]int{"a": 5})
	run("a = 3 - 2\n", "Subtraction assignment", map[string]int{"a": 1})
	run("a = 3 * 2\n", "Multiplication assignment", map[string]int{"a": 6})
	run("a = 6 / 2\n", "Division assignment", map[string]int{"a": 3})
	run("a = 3 + 2 + 1\n", "Multiple summation assignment", map[string]int{"a": 6})
	run("a = 3 * 2 + 1\n", "Multiplication and additon", map[string]int{"a": 7})
	run("a = 3 * 2\nb = 2\nc = a * b\n", "Multiplication of two variables",
		map[string]int{"a": 6, "b": 2, "c": 12})
	run("a = 2\na = 1\n", "Re-assignment", map[string]int{"a": 1})
	run("a = 2\na = a + 1\n", "Re-assignment (2)", map[string]int{"a": 3})
}
