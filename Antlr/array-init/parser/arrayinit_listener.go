// Code generated from ArrayInit.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // ArrayInit

import "github.com/antlr4-go/antlr/v4"

// ArrayInitListener is a complete listener for a parse tree produced by ArrayInitParser.
type ArrayInitListener interface {
	antlr.ParseTreeListener

	// EnterInit is called when entering the init production.
	EnterInit(c *InitContext)

	// EnterValue is called when entering the value production.
	EnterValue(c *ValueContext)

	// ExitInit is called when exiting the init production.
	ExitInit(c *InitContext)

	// ExitValue is called when exiting the value production.
	ExitValue(c *ValueContext)
}
