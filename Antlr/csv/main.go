package main

import (
	"fmt"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/csv/parser"
)

const EMPTY = ""

type CsvListener struct {
	parser.BaseCsvListener
	rows                  []map[string]string
	header                []string
	currentRowFieldValues []string
}

func NewCsvListener() *CsvListener {
	return &CsvListener{
		rows:                  []map[string]string{},
		header:                []string{},
		currentRowFieldValues: []string{},
	}
}

func (c *CsvListener) ExitHdr(ctx *parser.HdrContext) {
	c.header = make([]string, len(c.currentRowFieldValues))
	copy(c.header, c.currentRowFieldValues)
}

func (c *CsvListener) EnterRow(ctx *parser.RowContext) {
	c.currentRowFieldValues = []string{}
}

func (c *CsvListener) EnterField(ctx *parser.FieldContext) {
	text := ctx.GetText()
	fmt.Printf("text: %v\n", text)
	c.currentRowFieldValues = append(c.currentRowFieldValues, text)
}

func (c *CsvListener) ExitRow(ctx *parser.RowContext) {

	_, ok := ctx.GetParent().(*parser.HdrContext)
	if !ok {
		if len(c.currentRowFieldValues) != len(c.header) {
			panic(fmt.Sprintf("unexpected number of data elements (got %d, expected %d)",
				len(c.currentRowFieldValues), len(c.header)))
		}

		row := map[string]string{}
		for i := range c.header {
			row[c.header[i]] = c.currentRowFieldValues[i]
		}
		c.rows = append(c.rows, row)
	}
}

func main() {
	input := `Forename,Surname
Bob,Smith
Sally,Davies
`

	// Setup the input
	is := antlr.NewInputStream(input)

	// // Create the lexer
	lexer := parser.NewCsvLexer(is)

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

	fmt.Println("---")

	// Walk tree
	lexer.Reset()
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
	p := parser.NewCsvParser(stream)

	listener := NewCsvListener()
	antlr.ParseTreeWalkerDefault.Walk(listener, p.File())

	fmt.Printf("Header: %s\n", listener.header)
	fmt.Printf("Data: %s\n", listener.rows)
}
