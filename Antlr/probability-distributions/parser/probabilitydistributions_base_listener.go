// Code generated from ProbabilityDistributions.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // ProbabilityDistributions

import "github.com/antlr4-go/antlr/v4"

// BaseProbabilityDistributionsListener is a complete listener for a parse tree produced by ProbabilityDistributionsParser.
type BaseProbabilityDistributionsListener struct{}

var _ ProbabilityDistributionsListener = &BaseProbabilityDistributionsListener{}

// VisitTerminal is called when a terminal node is visited.
func (s *BaseProbabilityDistributionsListener) VisitTerminal(node antlr.TerminalNode) {}

// VisitErrorNode is called when an error node is visited.
func (s *BaseProbabilityDistributionsListener) VisitErrorNode(node antlr.ErrorNode) {}

// EnterEveryRule is called when any rule is entered.
func (s *BaseProbabilityDistributionsListener) EnterEveryRule(ctx antlr.ParserRuleContext) {}

// ExitEveryRule is called when any rule is exited.
func (s *BaseProbabilityDistributionsListener) ExitEveryRule(ctx antlr.ParserRuleContext) {}

// EnterProg is called when production prog is entered.
func (s *BaseProbabilityDistributionsListener) EnterProg(ctx *ProgContext) {}

// ExitProg is called when production prog is exited.
func (s *BaseProbabilityDistributionsListener) ExitProg(ctx *ProgContext) {}

// EnterAssign is called when production assign is entered.
func (s *BaseProbabilityDistributionsListener) EnterAssign(ctx *AssignContext) {}

// ExitAssign is called when production assign is exited.
func (s *BaseProbabilityDistributionsListener) ExitAssign(ctx *AssignContext) {}

// EnterPrint is called when production print is entered.
func (s *BaseProbabilityDistributionsListener) EnterPrint(ctx *PrintContext) {}

// ExitPrint is called when production print is exited.
func (s *BaseProbabilityDistributionsListener) ExitPrint(ctx *PrintContext) {}

// EnterBlank is called when production blank is entered.
func (s *BaseProbabilityDistributionsListener) EnterBlank(ctx *BlankContext) {}

// ExitBlank is called when production blank is exited.
func (s *BaseProbabilityDistributionsListener) ExitBlank(ctx *BlankContext) {}

// EnterParens is called when production parens is entered.
func (s *BaseProbabilityDistributionsListener) EnterParens(ctx *ParensContext) {}

// ExitParens is called when production parens is exited.
func (s *BaseProbabilityDistributionsListener) ExitParens(ctx *ParensContext) {}

// EnterExprDist is called when production exprDist is entered.
func (s *BaseProbabilityDistributionsListener) EnterExprDist(ctx *ExprDistContext) {}

// ExitExprDist is called when production exprDist is exited.
func (s *BaseProbabilityDistributionsListener) ExitExprDist(ctx *ExprDistContext) {}

// EnterMulDiv is called when production MulDiv is entered.
func (s *BaseProbabilityDistributionsListener) EnterMulDiv(ctx *MulDivContext) {}

// ExitMulDiv is called when production MulDiv is exited.
func (s *BaseProbabilityDistributionsListener) ExitMulDiv(ctx *MulDivContext) {}

// EnterAddSub is called when production AddSub is entered.
func (s *BaseProbabilityDistributionsListener) EnterAddSub(ctx *AddSubContext) {}

// ExitAddSub is called when production AddSub is exited.
func (s *BaseProbabilityDistributionsListener) ExitAddSub(ctx *AddSubContext) {}

// EnterId is called when production id is entered.
func (s *BaseProbabilityDistributionsListener) EnterId(ctx *IdContext) {}

// ExitId is called when production id is exited.
func (s *BaseProbabilityDistributionsListener) ExitId(ctx *IdContext) {}

// EnterNoisyMax is called when production NoisyMax is entered.
func (s *BaseProbabilityDistributionsListener) EnterNoisyMax(ctx *NoisyMaxContext) {}

// ExitNoisyMax is called when production NoisyMax is exited.
func (s *BaseProbabilityDistributionsListener) ExitNoisyMax(ctx *NoisyMaxContext) {}

// EnterDist is called when production dist is entered.
func (s *BaseProbabilityDistributionsListener) EnterDist(ctx *DistContext) {}

// ExitDist is called when production dist is exited.
func (s *BaseProbabilityDistributionsListener) ExitDist(ctx *DistContext) {}

// EnterElement is called when production element is entered.
func (s *BaseProbabilityDistributionsListener) EnterElement(ctx *ElementContext) {}

// ExitElement is called when production element is exited.
func (s *BaseProbabilityDistributionsListener) ExitElement(ctx *ElementContext) {}
