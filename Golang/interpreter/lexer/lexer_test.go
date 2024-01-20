package lexer

import (
	"fmt"
	"testing"

	"github.com/cdclaxton/monkey/token"
	"github.com/stretchr/testify/assert"
)

func TestNextToken(t *testing.T) {
	input := "=+(){},;"

	tests := []struct{
		expectedType token.TokenType
		expectedLiteral string
	}{
		{
			expectedType: token.ASSIGN,
			expectedLiteral: "=",
		},
		{
			expectedType: token.PLUS,
			expectedLiteral: "+",
		},
		{
			expectedType: token.LPAREN,
			expectedLiteral: "(",
		},
		{
			expectedType: token.RPAREN,
			expectedLiteral: ")",
		},
		{
			expectedType: token.LBRACE,
			expectedLiteral: "{",
		},
		{
			expectedType: token.RBRACE,
			expectedLiteral: "}",
		},
		{
			expectedType: token.COMMA,
			expectedLiteral: ",",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.EOF,
			expectedLiteral: "",
		},
	}

	l := New(input)

	for i, tt := range tests {
		t.Run(fmt.Sprintf("Test %d", i), func(t *testing.T) {
			tok := l.NextToken()

			assert.Equal(t, tt.expectedType, tok.Type)
			assert.Equal(t, tt.expectedLiteral, tok.Literal)
		})
	}
}

func TestNextToken2(t *testing.T) {
	input := `let five = 5;
let ten = 10;

let add = fn(x, y) {
	x + y;
};

let result = add(five, ten);
`

	tests := []struct{
		expectedType token.TokenType
		expectedLiteral string
	}{
		{
			expectedType: token.LET,
			expectedLiteral: "let",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "five",
		},
		{
			expectedType: token.ASSIGN,
			expectedLiteral: "=",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "5",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.LET,
			expectedLiteral: "let",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "ten",
		},
		{
			expectedType: token.ASSIGN,
			expectedLiteral: "=",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "10",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.LET,
			expectedLiteral: "let",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "add",
		},
		{
			expectedType: token.ASSIGN,
			expectedLiteral: "=",
		},
		{
			expectedType: token.FUNCTION,
			expectedLiteral: "fn",
		},
		{
			expectedType: token.LPAREN,
			expectedLiteral: "(",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "x",
		},
		{
			expectedType: token.COMMA,
			expectedLiteral: ",",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "y",
		},
		{
			expectedType: token.RPAREN,
			expectedLiteral: ")",
		},
		{
			expectedType: token.LBRACE,
			expectedLiteral: "{",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "x",
		},
		{
			expectedType: token.PLUS,
			expectedLiteral: "+",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "y",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.RBRACE,
			expectedLiteral: "}",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.LET,
			expectedLiteral: "let",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "result",
		},
		{
			expectedType: token.ASSIGN,
			expectedLiteral: "=",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "add",
		},
		{
			expectedType: token.LPAREN,
			expectedLiteral: "(",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "five",
		},
		{
			expectedType: token.COMMA,
			expectedLiteral: ",",
		},
		{
			expectedType: token.IDENT,
			expectedLiteral: "ten",
		},
		{
			expectedType: token.RPAREN,
			expectedLiteral: ")",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.EOF,
			expectedLiteral: "",
		},
	}

	l := New(input)

	for i, tt := range tests {
		t.Run(fmt.Sprintf("Test %d", i), func(t *testing.T) {
			tok := l.NextToken()

			assert.Equal(t, tt.expectedType, tok.Type)
			assert.Equal(t, tt.expectedLiteral, tok.Literal)
		})
	}
}

func TestNextToken3(t *testing.T) {
	input := `!-/*5;
5 < 10 > 5;	
`

	tests := []struct{
		expectedType token.TokenType
		expectedLiteral string
	}{
		{
			expectedType: token.BANG,
			expectedLiteral: "!",
		},
		{
			expectedType: token.MINUS,
			expectedLiteral: "-",
		},
		{
			expectedType: token.SLASH,
			expectedLiteral: "/",
		},
		{
			expectedType: token.ASTERISK,
			expectedLiteral: "*",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "5",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "5",
		},
		{
			expectedType: token.LT,
			expectedLiteral: "<",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "10",
		},
		{
			expectedType: token.GT,
			expectedLiteral: ">",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "5",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
	}

	l := New(input)

	for i, tt := range tests {
		t.Run(fmt.Sprintf("Test %d", i), func(t *testing.T) {
			tok := l.NextToken()

			assert.Equal(t, tt.expectedType, tok.Type)
			assert.Equal(t, tt.expectedLiteral, tok.Literal)
		})
	}
}

func TestNextToken4(t *testing.T) {
	input := `if (5 < 10) {
		return true;
	} else {
		return false;
}	
`

	tests := []struct{
		expectedType token.TokenType
		expectedLiteral string
	}{
		{
			expectedType: token.IF,
			expectedLiteral: "if",
		},
		{
			expectedType: token.LPAREN,
			expectedLiteral: "(",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "5",
		},
		{
			expectedType: token.LT,
			expectedLiteral: "<",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "10",
		},
		{
			expectedType: token.RPAREN,
			expectedLiteral: ")",
		},
		{
			expectedType: token.LBRACE,
			expectedLiteral: "{",
		},
		{
			expectedType: token.RETURN,
			expectedLiteral: "return",
		},
		{
			expectedType: token.TRUE,
			expectedLiteral: "true",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.RBRACE,
			expectedLiteral: "}",
		},
		{
			expectedType: token.ELSE,
			expectedLiteral: "else",
		},
		{
			expectedType: token.LBRACE,
			expectedLiteral: "{",
		},
		{
			expectedType: token.RETURN,
			expectedLiteral: "return",
		},
		{
			expectedType: token.FALSE,
			expectedLiteral: "false",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.RBRACE,
			expectedLiteral: "}",
		},
	}

	l := New(input)

	for i, tt := range tests {
		t.Run(fmt.Sprintf("Test %d", i), func(t *testing.T) {
			tok := l.NextToken()

			assert.Equal(t, tt.expectedType, tok.Type)
			assert.Equal(t, tt.expectedLiteral, tok.Literal)
		})
	}
}

func TestNextToken5(t *testing.T) {
	input := `10 == 10;
10 != 9;
`

	tests := []struct{
		expectedType token.TokenType
		expectedLiteral string
	}{
		{
			expectedType: token.INT,
			expectedLiteral: "10",
		},
		{
			expectedType: token.EQ,
			expectedLiteral: "==",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "10",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "10",
		},
		{
			expectedType: token.NOT_EQ,
			expectedLiteral: "!=",
		},
		{
			expectedType: token.INT,
			expectedLiteral: "9",
		},
		{
			expectedType: token.SEMICOLON,
			expectedLiteral: ";",
		},
	}

	l := New(input)

	for i, tt := range tests {
		t.Run(fmt.Sprintf("Test %d", i), func(t *testing.T) {
			tok := l.NextToken()

			assert.Equal(t, tt.expectedType, tok.Type)
			assert.Equal(t, tt.expectedLiteral, tok.Literal)
		})
	}
}