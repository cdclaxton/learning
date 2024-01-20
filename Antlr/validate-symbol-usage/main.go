package main

import (
	"os"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/validate-symbol-usage/parser"
)

func main() {

	// Read the program from file
	filename := "./program1.cymbol"
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err.Error())
	}

	program := string(bytes)
	is := antlr.NewInputStream(program)

	// Create the lexer
	lexer := parser.NewCymbolLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)

	// Create the parser
	p := parser.NewCymbolParser(stream)

	// Create the listener
	listener := NewCallGraphListener()
	antlr.ParseTreeWalkerDefault.Walk(listener, p.File())

}
