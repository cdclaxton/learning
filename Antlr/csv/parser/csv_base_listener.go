// Code generated from Csv.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // Csv

import "github.com/antlr4-go/antlr/v4"

// BaseCsvListener is a complete listener for a parse tree produced by CsvParser.
type BaseCsvListener struct{}

var _ CsvListener = &BaseCsvListener{}

// VisitTerminal is called when a terminal node is visited.
func (s *BaseCsvListener) VisitTerminal(node antlr.TerminalNode) {}

// VisitErrorNode is called when an error node is visited.
func (s *BaseCsvListener) VisitErrorNode(node antlr.ErrorNode) {}

// EnterEveryRule is called when any rule is entered.
func (s *BaseCsvListener) EnterEveryRule(ctx antlr.ParserRuleContext) {}

// ExitEveryRule is called when any rule is exited.
func (s *BaseCsvListener) ExitEveryRule(ctx antlr.ParserRuleContext) {}

// EnterFile is called when production file is entered.
func (s *BaseCsvListener) EnterFile(ctx *FileContext) {}

// ExitFile is called when production file is exited.
func (s *BaseCsvListener) ExitFile(ctx *FileContext) {}

// EnterHdr is called when production hdr is entered.
func (s *BaseCsvListener) EnterHdr(ctx *HdrContext) {}

// ExitHdr is called when production hdr is exited.
func (s *BaseCsvListener) ExitHdr(ctx *HdrContext) {}

// EnterRow is called when production row is entered.
func (s *BaseCsvListener) EnterRow(ctx *RowContext) {}

// ExitRow is called when production row is exited.
func (s *BaseCsvListener) ExitRow(ctx *RowContext) {}

// EnterField is called when production field is entered.
func (s *BaseCsvListener) EnterField(ctx *FieldContext) {}

// ExitField is called when production field is exited.
func (s *BaseCsvListener) ExitField(ctx *FieldContext) {}
