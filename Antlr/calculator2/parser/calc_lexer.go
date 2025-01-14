// Code generated from Calc.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser

import (
	"fmt"
	"github.com/antlr4-go/antlr/v4"
	"sync"
	"unicode"
)

// Suppress unused import error
var _ = fmt.Printf
var _ = sync.Once{}
var _ = unicode.IsLetter

type CalcLexer struct {
	*antlr.BaseLexer
	channelNames []string
	modeNames    []string
	// TODO: EOF string
}

var CalcLexerLexerStaticData struct {
	once                   sync.Once
	serializedATN          []int32
	ChannelNames           []string
	ModeNames              []string
	LiteralNames           []string
	SymbolicNames          []string
	RuleNames              []string
	PredictionContextCache *antlr.PredictionContextCache
	atn                    *antlr.ATN
	decisionToDFA          []*antlr.DFA
}

func calclexerLexerInit() {
	staticData := &CalcLexerLexerStaticData
	staticData.ChannelNames = []string{
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN",
	}
	staticData.ModeNames = []string{
		"DEFAULT_MODE",
	}
	staticData.LiteralNames = []string{
		"", "'('", "')'", "'+'", "'-'", "'*'", "'/'",
	}
	staticData.SymbolicNames = []string{
		"", "", "", "ADD", "SUB", "MUL", "DIV", "NUMBER", "WS",
	}
	staticData.RuleNames = []string{
		"T__0", "T__1", "ADD", "SUB", "MUL", "DIV", "NUMBER", "WS",
	}
	staticData.PredictionContextCache = antlr.NewPredictionContextCache()
	staticData.serializedATN = []int32{
		4, 0, 8, 49, 6, -1, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2,
		4, 7, 4, 2, 5, 7, 5, 2, 6, 7, 6, 2, 7, 7, 7, 1, 0, 1, 0, 1, 1, 1, 1, 1,
		2, 1, 2, 1, 3, 1, 3, 1, 4, 1, 4, 1, 5, 1, 5, 1, 6, 4, 6, 31, 8, 6, 11,
		6, 12, 6, 32, 1, 6, 1, 6, 4, 6, 37, 8, 6, 11, 6, 12, 6, 38, 3, 6, 41, 8,
		6, 1, 7, 4, 7, 44, 8, 7, 11, 7, 12, 7, 45, 1, 7, 1, 7, 0, 0, 8, 1, 1, 3,
		2, 5, 3, 7, 4, 9, 5, 11, 6, 13, 7, 15, 8, 1, 0, 2, 1, 0, 48, 57, 3, 0,
		9, 10, 13, 13, 32, 32, 52, 0, 1, 1, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 5, 1,
		0, 0, 0, 0, 7, 1, 0, 0, 0, 0, 9, 1, 0, 0, 0, 0, 11, 1, 0, 0, 0, 0, 13,
		1, 0, 0, 0, 0, 15, 1, 0, 0, 0, 1, 17, 1, 0, 0, 0, 3, 19, 1, 0, 0, 0, 5,
		21, 1, 0, 0, 0, 7, 23, 1, 0, 0, 0, 9, 25, 1, 0, 0, 0, 11, 27, 1, 0, 0,
		0, 13, 30, 1, 0, 0, 0, 15, 43, 1, 0, 0, 0, 17, 18, 5, 40, 0, 0, 18, 2,
		1, 0, 0, 0, 19, 20, 5, 41, 0, 0, 20, 4, 1, 0, 0, 0, 21, 22, 5, 43, 0, 0,
		22, 6, 1, 0, 0, 0, 23, 24, 5, 45, 0, 0, 24, 8, 1, 0, 0, 0, 25, 26, 5, 42,
		0, 0, 26, 10, 1, 0, 0, 0, 27, 28, 5, 47, 0, 0, 28, 12, 1, 0, 0, 0, 29,
		31, 7, 0, 0, 0, 30, 29, 1, 0, 0, 0, 31, 32, 1, 0, 0, 0, 32, 30, 1, 0, 0,
		0, 32, 33, 1, 0, 0, 0, 33, 40, 1, 0, 0, 0, 34, 36, 5, 46, 0, 0, 35, 37,
		7, 0, 0, 0, 36, 35, 1, 0, 0, 0, 37, 38, 1, 0, 0, 0, 38, 36, 1, 0, 0, 0,
		38, 39, 1, 0, 0, 0, 39, 41, 1, 0, 0, 0, 40, 34, 1, 0, 0, 0, 40, 41, 1,
		0, 0, 0, 41, 14, 1, 0, 0, 0, 42, 44, 7, 1, 0, 0, 43, 42, 1, 0, 0, 0, 44,
		45, 1, 0, 0, 0, 45, 43, 1, 0, 0, 0, 45, 46, 1, 0, 0, 0, 46, 47, 1, 0, 0,
		0, 47, 48, 6, 7, 0, 0, 48, 16, 1, 0, 0, 0, 5, 0, 32, 38, 40, 45, 1, 6,
		0, 0,
	}
	deserializer := antlr.NewATNDeserializer(nil)
	staticData.atn = deserializer.Deserialize(staticData.serializedATN)
	atn := staticData.atn
	staticData.decisionToDFA = make([]*antlr.DFA, len(atn.DecisionToState))
	decisionToDFA := staticData.decisionToDFA
	for index, state := range atn.DecisionToState {
		decisionToDFA[index] = antlr.NewDFA(state, index)
	}
}

// CalcLexerInit initializes any static state used to implement CalcLexer. By default the
// static state used to implement the lexer is lazily initialized during the first call to
// NewCalcLexer(). You can call this function if you wish to initialize the static state ahead
// of time.
func CalcLexerInit() {
	staticData := &CalcLexerLexerStaticData
	staticData.once.Do(calclexerLexerInit)
}

// NewCalcLexer produces a new lexer instance for the optional input antlr.CharStream.
func NewCalcLexer(input antlr.CharStream) *CalcLexer {
	CalcLexerInit()
	l := new(CalcLexer)
	l.BaseLexer = antlr.NewBaseLexer(input)
	staticData := &CalcLexerLexerStaticData
	l.Interpreter = antlr.NewLexerATNSimulator(l, staticData.atn, staticData.decisionToDFA, staticData.PredictionContextCache)
	l.channelNames = staticData.ChannelNames
	l.modeNames = staticData.ModeNames
	l.RuleNames = staticData.RuleNames
	l.LiteralNames = staticData.LiteralNames
	l.SymbolicNames = staticData.SymbolicNames
	l.GrammarFileName = "Calc.g4"
	// TODO: l.EOF = antlr.TokenEOF

	return l
}

// CalcLexer tokens.
const (
	CalcLexerT__0   = 1
	CalcLexerT__1   = 2
	CalcLexerADD    = 3
	CalcLexerSUB    = 4
	CalcLexerMUL    = 5
	CalcLexerDIV    = 6
	CalcLexerNUMBER = 7
	CalcLexerWS     = 8
)
