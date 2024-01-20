package parser

import (
	"fmt"
	"testing"

	"github.com/cdclaxton/monkey/ast"
	"github.com/cdclaxton/monkey/lexer"
	"github.com/stretchr/testify/assert"
)

func testLetStatement(t *testing.T, s ast.Statement, name string) {
	assert.Equal(t, "let", s.TokenLiteral())

	letStmt, ok := s.(*ast.LetStatement)
	assert.True(t, ok)
	assert.Equal(t, name, letStmt.Name.Value)
	assert.Equal(t, name, letStmt.Name.TokenLiteral())
}

func checkParseErrors(t *testing.T, p *Parser) {
	errors := p.Errors()
	if len(errors) == 0 {
		return
	}

	t.Errorf("parser has %d errors", len(errors))
	for _, msg := range errors {
		t.Errorf("parser error: %q", msg)
	}
	t.FailNow()
}

func TestLetStatements(t *testing.T) {
	input := `
let x = 5;
let y = 10;
let foobar = 838383;`

	l := lexer.New(input)
	p := New(l)

	program := p.ParseProgram()
	assert.NotNil(t, program)
	assert.Len(t, program.Statements, 3)

	checkParseErrors(t, p)

	tests := []struct {
		expectedIdentifier string
	}{
		{
			expectedIdentifier: "x",
		},
		{
			expectedIdentifier: "y",
		},
		{
			expectedIdentifier: "foobar",
		},
	}

	for i, tt := range tests {
		stmt := program.Statements[i]
		testLetStatement(t, stmt, tt.expectedIdentifier)
	}
}

func TestReturnStatements(t *testing.T) {
	input := `
return 5;
return 10;
return 1000;	
`

	l := lexer.New(input)
	p := New(l)

	program := p.ParseProgram()
	checkParseErrors(t, p)

	assert.Len(t, program.Statements, 3)
	for _, stmt := range program.Statements {
		returnStmt, ok := stmt.(*ast.ReturnStatement)
		assert.True(t, ok)
		assert.Equal(t, "return", returnStmt.TokenLiteral())
	}
}

func TestIdentifierExpression(t *testing.T) {
	input := "foobar;"

	l := lexer.New(input)
	p := New(l)

	program := p.ParseProgram()
	checkParseErrors(t, p)

	assert.Len(t, program.Statements, 1)

	stmt, ok := program.Statements[0].(*ast.ExpressionStatement)
	assert.True(t, ok)

	ident, ok := stmt.Expression.(*ast.Identifier)
	assert.True(t, ok)
	assert.Equal(t, "foobar", ident.Value)
	assert.Equal(t, "foobar", ident.TokenLiteral())
}

func TestIntegerLiteralExpression(t *testing.T) {
	input := "5;"

	l := lexer.New(input)
	p := New(l)

	program := p.ParseProgram()
	checkParseErrors(t, p)

	assert.Len(t, program.Statements, 1)

	stmt, ok := program.Statements[0].(*ast.ExpressionStatement)
	assert.True(t, ok)

	literal, ok := stmt.Expression.(*ast.IntegerLiteral)
	assert.True(t, ok)
	assert.Equal(t, int64(5), literal.Value)
	assert.Equal(t, "5", literal.TokenLiteral())
}

func testIntegerLiteral(t *testing.T, il ast.Expression, value int64) {
	integ, ok := il.(*ast.IntegerLiteral)
	assert.True(t, ok)
	assert.Equal(t, value, integ.Value)
	assert.Equal(t, fmt.Sprintf("%d", value), integ.TokenLiteral())
}

func TestParsingPrefixExpression(t *testing.T) {
	prefixTests := []struct {
		input        string
		operator     string
		integerValue int64
	}{
		{
			input:        "!5",
			operator:     "!",
			integerValue: int64(5),
		},
		{
			input:        "-15",
			operator:     "-",
			integerValue: int64(15),
		},
	}

	for _, tt := range prefixTests {
		l := lexer.New(tt.input)
		p := New(l)

		program := p.ParseProgram()
		checkParseErrors(t, p)

		assert.Len(t, program.Statements, 1)

		stmt, ok := program.Statements[0].(*ast.ExpressionStatement)
		assert.True(t, ok)

		exp, ok := stmt.Expression.(*ast.PrefixExpression)
		assert.True(t, ok)
		assert.Equal(t, tt.operator, exp.Operator)
		testIntegerLiteral(t, exp.Right, tt.integerValue)
	}
}

func TestParsingInfixExpressions(t *testing.T) {
	infixTests := []struct {
		input      string
		leftValue  int64
		operator   string
		rightValue int64
	}{
		{
			input:      "5 + 5;",
			leftValue:  int64(5),
			operator:   "+",
			rightValue: int64(5),
		},
		{
			input:      "5 - 5;",
			leftValue:  int64(5),
			operator:   "-",
			rightValue: int64(5),
		},
		{
			input:      "5 * 5;",
			leftValue:  int64(5),
			operator:   "*",
			rightValue: int64(5),
		},
		{
			input:      "5 / 5;",
			leftValue:  int64(5),
			operator:   "/",
			rightValue: int64(5),
		},
		{
			input:      "5 > 5;",
			leftValue:  int64(5),
			operator:   ">",
			rightValue: int64(5),
		},
		{
			input:      "5 < 5;",
			leftValue:  int64(5),
			operator:   "<",
			rightValue: int64(5),
		},
		{
			input:      "5 == 5;",
			leftValue:  int64(5),
			operator:   "==",
			rightValue: int64(5),
		},
		{
			input:      "5 != 5;",
			leftValue:  int64(5),
			operator:   "!=",
			rightValue: int64(5),
		},
	}

	for _, tt := range infixTests {
		l := lexer.New(tt.input)
		p := New(l)

		program := p.ParseProgram()
		checkParseErrors(t, p)

		assert.Len(t, program.Statements, 1)

		stmt, ok := program.Statements[0].(*ast.ExpressionStatement)
		assert.True(t, ok)

		exp, ok := stmt.Expression.(*ast.InfixExpression)
		assert.True(t, ok)
		testIntegerLiteral(t, exp.Left, tt.leftValue)

		assert.Equal(t, tt.operator, exp.Operator)

		testIntegerLiteral(t, exp.Right, tt.rightValue)
	}
}

func TestOperatorPrecedenceParsing(t *testing.T) {
	tests := []struct {
		input  string
		output string
	}{
		{
			input:  "-a * b",
			output: "((-a) * b)",
		},
		{
			input:  "!-a",
			output: "(!(-a))",
		},
		{
			input:  "a + b + c",
			output: "((a + b) + c)",
		},
		{
			input:  "a + b - c",
			output: "((a + b) - c)",
		},
		{
			input:  "a * b * c",
			output: "((a * b) * c)",
		},
		{
			input:  "a * b / c",
			output: "((a * b) / c)",
		},
		{
			input:  "a + b * c + d / e - f",
			output: "(((a + (b * c)) + (d / e)) - f)",
		},
		{
			input:  "3 + 4; -5 * 5;",
			output: "(3 + 4)((-5) * 5)",
		},
		{
			input:  "5 > 4 == 3 < 4",
			output: "((5 > 4) == (3 < 4))",
		},
		{
			input:  "5 < 4 != 3 > 4",
			output: "((5 < 4) != (3 > 4))",
		},
		{
			input:  "3 + 4 * 5 == 3 * 1 + 4 * 5",
			output: "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))",
		},
	}

	for _, tt := range tests {
		l := lexer.New(tt.input)
		p := New(l)

		program := p.ParseProgram()
		checkParseErrors(t, p)

		assert.Equal(t, tt.output, program.String())
	}
}

func testIdentifier(t *testing.T, exp ast.Expression, value string) {
	ident, ok := exp.(*ast.Identifier)
	assert.True(t, ok)

	assert.Equal(t, value, ident.Value)
	assert.Equal(t, value, ident.TokenLiteral())
}

func testLiteralExpression(t *testing.T, exp ast.Expression, expected interface{}) {
	switch v := expected.(type) {
	case int:
		testIntegerLiteral(t, exp, int64(v))
	case int64:
		testIntegerLiteral(t, exp, v)
	case string:
		testIdentifier(t, exp, v)
	}

	t.Errorf("type of exp not handled: %T", exp)
}

func testInfixExpression(t *testing.T, exp ast.Expression, left interface{},
	operator string, right interface{}) {

	opExp, ok := exp.(*ast.InfixExpression)
	assert.True(t, ok)

	testLiteralExpression(t, opExp.Left, left)

	assert.Equal(t, operator, opExp.Operator)

	testLiteralExpression(t, opExp.Right, right)
}
