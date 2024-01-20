package main

import (
	"fmt"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/expr/parser"
)

type evalListener struct {
	parser.BaseExprListener
	memory map[string]int
}

func newEvalListener() *evalListener {
	return &evalListener{
		memory: map[string]int{},
	}
}

func (e *evalListener) EnterProg(ctx *parser.ProgContext) {
	fmt.Printf("entering prog ...\n")
}

func (e *evalListener) ExitAssign(ctx *parser.AssignContext) {
	fmt.Printf("assign (%s)\n", ctx.GetText())
	// id := ctx.ID().GetText()

	// fmt.Printf("Setting %s = %s\n", id, ctx.Expr().GetText())
}

func (e *evalListener) ExitId(ctx *parser.IdContext) {
	fmt.Printf("id (%s)\n", ctx.GetText())
}

func (e *evalListener) ExitInt(ctx *parser.IntContext) {
	fmt.Printf("int (%s)\n", ctx.GetText())
}

func main() {
	// Setup the input
	is := antlr.NewInputStream("a = 3\n")

	// Create the lexer
	lexer := parser.NewExprLexer(is)

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

	fmt.Println("---")

	// Walk tree
	lexer.Reset()
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
	p := parser.NewExprParser(stream)

	listener := newEvalListener()
	antlr.ParseTreeWalkerDefault.Walk(listener, p.Prog())
}
