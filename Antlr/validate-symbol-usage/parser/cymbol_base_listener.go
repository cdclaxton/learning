// Code generated from Cymbol.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // Cymbol

import "github.com/antlr4-go/antlr/v4"

// BaseCymbolListener is a complete listener for a parse tree produced by CymbolParser.
type BaseCymbolListener struct{}

var _ CymbolListener = &BaseCymbolListener{}

// VisitTerminal is called when a terminal node is visited.
func (s *BaseCymbolListener) VisitTerminal(node antlr.TerminalNode) {}

// VisitErrorNode is called when an error node is visited.
func (s *BaseCymbolListener) VisitErrorNode(node antlr.ErrorNode) {}

// EnterEveryRule is called when any rule is entered.
func (s *BaseCymbolListener) EnterEveryRule(ctx antlr.ParserRuleContext) {}

// ExitEveryRule is called when any rule is exited.
func (s *BaseCymbolListener) ExitEveryRule(ctx antlr.ParserRuleContext) {}

// EnterFile is called when production file is entered.
func (s *BaseCymbolListener) EnterFile(ctx *FileContext) {}

// ExitFile is called when production file is exited.
func (s *BaseCymbolListener) ExitFile(ctx *FileContext) {}

// EnterVarDecl is called when production varDecl is entered.
func (s *BaseCymbolListener) EnterVarDecl(ctx *VarDeclContext) {}

// ExitVarDecl is called when production varDecl is exited.
func (s *BaseCymbolListener) ExitVarDecl(ctx *VarDeclContext) {}

// EnterType is called when production type is entered.
func (s *BaseCymbolListener) EnterType(ctx *TypeContext) {}

// ExitType is called when production type is exited.
func (s *BaseCymbolListener) ExitType(ctx *TypeContext) {}

// EnterFunctionDecl is called when production functionDecl is entered.
func (s *BaseCymbolListener) EnterFunctionDecl(ctx *FunctionDeclContext) {}

// ExitFunctionDecl is called when production functionDecl is exited.
func (s *BaseCymbolListener) ExitFunctionDecl(ctx *FunctionDeclContext) {}

// EnterFormalParameters is called when production formalParameters is entered.
func (s *BaseCymbolListener) EnterFormalParameters(ctx *FormalParametersContext) {}

// ExitFormalParameters is called when production formalParameters is exited.
func (s *BaseCymbolListener) ExitFormalParameters(ctx *FormalParametersContext) {}

// EnterFormalParameter is called when production formalParameter is entered.
func (s *BaseCymbolListener) EnterFormalParameter(ctx *FormalParameterContext) {}

// ExitFormalParameter is called when production formalParameter is exited.
func (s *BaseCymbolListener) ExitFormalParameter(ctx *FormalParameterContext) {}

// EnterBlock is called when production block is entered.
func (s *BaseCymbolListener) EnterBlock(ctx *BlockContext) {}

// ExitBlock is called when production block is exited.
func (s *BaseCymbolListener) ExitBlock(ctx *BlockContext) {}

// EnterStat is called when production stat is entered.
func (s *BaseCymbolListener) EnterStat(ctx *StatContext) {}

// ExitStat is called when production stat is exited.
func (s *BaseCymbolListener) ExitStat(ctx *StatContext) {}

// EnterCall is called when production Call is entered.
func (s *BaseCymbolListener) EnterCall(ctx *CallContext) {}

// ExitCall is called when production Call is exited.
func (s *BaseCymbolListener) ExitCall(ctx *CallContext) {}

// EnterNot is called when production Not is entered.
func (s *BaseCymbolListener) EnterNot(ctx *NotContext) {}

// ExitNot is called when production Not is exited.
func (s *BaseCymbolListener) ExitNot(ctx *NotContext) {}

// EnterMult is called when production Mult is entered.
func (s *BaseCymbolListener) EnterMult(ctx *MultContext) {}

// ExitMult is called when production Mult is exited.
func (s *BaseCymbolListener) ExitMult(ctx *MultContext) {}

// EnterAddSub is called when production AddSub is entered.
func (s *BaseCymbolListener) EnterAddSub(ctx *AddSubContext) {}

// ExitAddSub is called when production AddSub is exited.
func (s *BaseCymbolListener) ExitAddSub(ctx *AddSubContext) {}

// EnterEqual is called when production Equal is entered.
func (s *BaseCymbolListener) EnterEqual(ctx *EqualContext) {}

// ExitEqual is called when production Equal is exited.
func (s *BaseCymbolListener) ExitEqual(ctx *EqualContext) {}

// EnterVar is called when production Var is entered.
func (s *BaseCymbolListener) EnterVar(ctx *VarContext) {}

// ExitVar is called when production Var is exited.
func (s *BaseCymbolListener) ExitVar(ctx *VarContext) {}

// EnterParens is called when production Parens is entered.
func (s *BaseCymbolListener) EnterParens(ctx *ParensContext) {}

// ExitParens is called when production Parens is exited.
func (s *BaseCymbolListener) ExitParens(ctx *ParensContext) {}

// EnterIndex is called when production Index is entered.
func (s *BaseCymbolListener) EnterIndex(ctx *IndexContext) {}

// ExitIndex is called when production Index is exited.
func (s *BaseCymbolListener) ExitIndex(ctx *IndexContext) {}

// EnterNegate is called when production Negate is entered.
func (s *BaseCymbolListener) EnterNegate(ctx *NegateContext) {}

// ExitNegate is called when production Negate is exited.
func (s *BaseCymbolListener) ExitNegate(ctx *NegateContext) {}

// EnterInt is called when production Int is entered.
func (s *BaseCymbolListener) EnterInt(ctx *IntContext) {}

// ExitInt is called when production Int is exited.
func (s *BaseCymbolListener) ExitInt(ctx *IntContext) {}

// EnterExprList is called when production exprList is entered.
func (s *BaseCymbolListener) EnterExprList(ctx *ExprListContext) {}

// ExitExprList is called when production exprList is exited.
func (s *BaseCymbolListener) ExitExprList(ctx *ExprListContext) {}
