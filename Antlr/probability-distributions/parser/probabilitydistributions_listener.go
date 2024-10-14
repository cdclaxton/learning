// Code generated from ProbabilityDistributions.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // ProbabilityDistributions

import "github.com/antlr4-go/antlr/v4"

// ProbabilityDistributionsListener is a complete listener for a parse tree produced by ProbabilityDistributionsParser.
type ProbabilityDistributionsListener interface {
	antlr.ParseTreeListener

	// EnterProg is called when entering the prog production.
	EnterProg(c *ProgContext)

	// EnterAssign is called when entering the assign production.
	EnterAssign(c *AssignContext)

	// EnterBlank is called when entering the blank production.
	EnterBlank(c *BlankContext)

	// EnterExprDist is called when entering the exprDist production.
	EnterExprDist(c *ExprDistContext)

	// EnterMulDiv is called when entering the MulDiv production.
	EnterMulDiv(c *MulDivContext)

	// EnterAddSub is called when entering the AddSub production.
	EnterAddSub(c *AddSubContext)

	// EnterId is called when entering the id production.
	EnterId(c *IdContext)

	// EnterDist is called when entering the dist production.
	EnterDist(c *DistContext)

	// EnterElement is called when entering the element production.
	EnterElement(c *ElementContext)

	// ExitProg is called when exiting the prog production.
	ExitProg(c *ProgContext)

	// ExitAssign is called when exiting the assign production.
	ExitAssign(c *AssignContext)

	// ExitBlank is called when exiting the blank production.
	ExitBlank(c *BlankContext)

	// ExitExprDist is called when exiting the exprDist production.
	ExitExprDist(c *ExprDistContext)

	// ExitMulDiv is called when exiting the MulDiv production.
	ExitMulDiv(c *MulDivContext)

	// ExitAddSub is called when exiting the AddSub production.
	ExitAddSub(c *AddSubContext)

	// ExitId is called when exiting the id production.
	ExitId(c *IdContext)

	// ExitDist is called when exiting the dist production.
	ExitDist(c *DistContext)

	// ExitElement is called when exiting the element production.
	ExitElement(c *ElementContext)
}
