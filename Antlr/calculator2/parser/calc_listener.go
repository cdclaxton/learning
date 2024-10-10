// Code generated from Calc.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // Calc

import "github.com/antlr4-go/antlr/v4"

// CalcListener is a complete listener for a parse tree produced by CalcParser.
type CalcListener interface {
	antlr.ParseTreeListener

	// EnterExpr is called when entering the expr production.
	EnterExpr(c *ExprContext)

	// EnterTerm is called when entering the term production.
	EnterTerm(c *TermContext)

	// EnterNumber is called when entering the Number production.
	EnterNumber(c *NumberContext)

	// EnterExpression is called when entering the Expression production.
	EnterExpression(c *ExpressionContext)

	// EnterUnaryFactor is called when entering the UnaryFactor production.
	EnterUnaryFactor(c *UnaryFactorContext)

	// ExitExpr is called when exiting the expr production.
	ExitExpr(c *ExprContext)

	// ExitTerm is called when exiting the term production.
	ExitTerm(c *TermContext)

	// ExitNumber is called when exiting the Number production.
	ExitNumber(c *NumberContext)

	// ExitExpression is called when exiting the Expression production.
	ExitExpression(c *ExpressionContext)

	// ExitUnaryFactor is called when exiting the UnaryFactor production.
	ExitUnaryFactor(c *UnaryFactorContext)
}
