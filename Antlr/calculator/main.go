package main

import (
	"fmt"
	"strconv"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/calculator/parser"
)

type calcListener struct {
	*parser.BaseCalcListener

	stack []int
}

func (l *calcListener) push(i int) {
	l.stack = append(l.stack, i)
}

func (l *calcListener) pop() int {
	if len(l.stack) < 1 {
		panic("stack is empty, unable to pop")
	}

	// Get the last value from the stack
	result := l.stack[len(l.stack)-1]

	// Remove the last element from the stack
	l.stack = l.stack[:len(l.stack)-1]

	return result
}

func (l *calcListener) ExitMulDiv(c *parser.MulDivContext) {
	right, left := l.pop(), l.pop()

	switch c.GetOp().GetTokenType() {
	case parser.CalcParserMUL:
		l.push(left * right)
	case parser.CalcParserDIV:
		l.push(left / right)
	default:
		panic(fmt.Sprintf("unexpected op: %s", c.GetOp().GetText()))
	}
}

func (l *calcListener) ExitAddSub(c *parser.AddSubContext) {
	right, left := l.pop(), l.pop()

	switch c.GetOp().GetTokenType() {
	case parser.CalcParserADD:
		l.push(left + right)
	case parser.CalcParserSUB:
		l.push(left - right)
	default:
		panic(fmt.Sprintf("unexpected op: %s", c.GetOp().GetText()))
	}
}

func (l *calcListener) ExitNumber(c *parser.NumberContext) {
	i, err := strconv.Atoi(c.GetText())
	if err != nil {
		panic(err.Error())
	}

	l.push(i)
}

func main() {
	// Setup the input
	is := antlr.NewInputStream("1 + 2 * 3")

	// Create the lexer
	lexer := parser.NewCalcLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)

	// Read all tokens
	for {
		t := lexer.NextToken()
		if t.GetTokenType() == antlr.TokenEOF {
			break
		}

		// Token type is an integer representing the type of token
		// Text is the literal
		fmt.Printf("%s (%q)\n",
			lexer.SymbolicNames[t.GetTokenType()], t.GetText())
	}

	// Create the parser
	lexer.Reset()
	p := parser.NewCalcParser(stream)

	// Parse the expression by walking the tree
	var listener calcListener
	antlr.ParseTreeWalkerDefault.Walk(&listener, p.Start_())

	fmt.Printf("Result: %d\n", listener.pop())
}
