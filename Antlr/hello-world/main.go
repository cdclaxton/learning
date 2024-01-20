package main

import (
	"fmt"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/hello-world/parser"
)

func main() {
	fmt.Println("Hello, World! ANTLR example")

	// Setup the input
	is := antlr.NewInputStream("hello chris this is an example")

	// Create the lexer
	lexer := parser.NewHelloLexer(is)

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
}
