// Code generated from Csv.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // Csv

import "github.com/antlr4-go/antlr/v4"

// CsvListener is a complete listener for a parse tree produced by CsvParser.
type CsvListener interface {
	antlr.ParseTreeListener

	// EnterFile is called when entering the file production.
	EnterFile(c *FileContext)

	// EnterHdr is called when entering the hdr production.
	EnterHdr(c *HdrContext)

	// EnterRow is called when entering the row production.
	EnterRow(c *RowContext)

	// EnterField is called when entering the field production.
	EnterField(c *FieldContext)

	// ExitFile is called when exiting the file production.
	ExitFile(c *FileContext)

	// ExitHdr is called when exiting the hdr production.
	ExitHdr(c *HdrContext)

	// ExitRow is called when exiting the row production.
	ExitRow(c *RowContext)

	// ExitField is called when exiting the field production.
	ExitField(c *FieldContext)
}
