package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/array-init/parser"
)

type arrayInitListener struct {
	*parser.BaseArrayInitListener
	str strings.Builder
}

func newArrayInitListener() arrayInitListener {
	return arrayInitListener{
		str: strings.Builder{},
	}
}

func (a *arrayInitListener) EnterInit(ctx *parser.InitContext) {
	a.str.WriteString("\"")
}
func (a *arrayInitListener) ExitInit(ctx *parser.InitContext) {
	a.str.WriteString("\"")
}

func (a *arrayInitListener) EnterValue(ctx *parser.ValueContext) {

	if len(ctx.GetTokens(parser.ArrayInitLexerINT)) > 0 {
		s := ctx.INT().GetText()
		value, err := strconv.Atoi(s)
		if err != nil {
			panic(err.Error())
		}

		a.str.WriteString(fmt.Sprintf("%04x", value))
	}

}

func main() {

	// Setup the input
	is := antlr.NewInputStream("{1, {15, 20}, 2}")

	// Create the lexer
	lexer := parser.NewArrayInitLexer(is)

	// Read all tokens
	for {
		t := lexer.NextToken()
		if t.GetTokenType() == antlr.TokenEOF {
			break
		}

		fmt.Printf("Line: %d, Start: %d, Stop: %d, Token ID: %d, Token type: %s, Text: %q\n",
			t.GetLine(),
			t.GetStart(),
			t.GetStop(),
			t.GetTokenType(),
			lexer.SymbolicNames[t.GetTokenType()],
			t.GetText())
	}

	lexer.Reset()
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
	p := parser.NewArrayInitParser(stream)

	listener := newArrayInitListener()
	antlr.ParseTreeWalkerDefault.Walk(&listener, p.Init())

	fmt.Printf("Result: %s\n", listener.str.String())
}
