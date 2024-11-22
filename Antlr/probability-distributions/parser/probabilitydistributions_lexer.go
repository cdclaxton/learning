// Code generated from ProbabilityDistributions.g4 by ANTLR 4.13.1. DO NOT EDIT.

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

type ProbabilityDistributionsLexer struct {
	*antlr.BaseLexer
	channelNames []string
	modeNames    []string
	// TODO: EOF string
}

var ProbabilityDistributionsLexerLexerStaticData struct {
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

func probabilitydistributionslexerLexerInit() {
	staticData := &ProbabilityDistributionsLexerLexerStaticData
	staticData.ChannelNames = []string{
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN",
	}
	staticData.ModeNames = []string{
		"DEFAULT_MODE",
	}
	staticData.LiteralNames = []string{
		"", "'='", "'('", "')'", "'{'", "','", "'}'", "':'", "", "", "", "",
		"", "'*'", "'/'", "'+'", "'-'", "'|'",
	}
	staticData.SymbolicNames = []string{
		"", "", "", "", "", "", "", "", "ID", "INT", "FLOAT", "NEWLINE", "WS",
		"MUL", "DIV", "ADD", "SUB", "OR",
	}
	staticData.RuleNames = []string{
		"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "ID", "INT",
		"FLOAT", "NEWLINE", "WS", "MUL", "DIV", "ADD", "SUB", "OR",
	}
	staticData.PredictionContextCache = antlr.NewPredictionContextCache()
	staticData.serializedATN = []int32{
		4, 0, 17, 95, 6, -1, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2,
		4, 7, 4, 2, 5, 7, 5, 2, 6, 7, 6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2,
		10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13, 2, 14, 7, 14, 2, 15,
		7, 15, 2, 16, 7, 16, 1, 0, 1, 0, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 1, 3, 1,
		4, 1, 4, 1, 5, 1, 5, 1, 6, 1, 6, 1, 7, 4, 7, 51, 8, 7, 11, 7, 12, 7, 52,
		1, 8, 4, 8, 56, 8, 8, 11, 8, 12, 8, 57, 1, 9, 4, 9, 61, 8, 9, 11, 9, 12,
		9, 62, 1, 9, 1, 9, 5, 9, 67, 8, 9, 10, 9, 12, 9, 70, 9, 9, 3, 9, 72, 8,
		9, 1, 10, 3, 10, 75, 8, 10, 1, 10, 1, 10, 1, 11, 4, 11, 80, 8, 11, 11,
		11, 12, 11, 81, 1, 11, 1, 11, 1, 12, 1, 12, 1, 13, 1, 13, 1, 14, 1, 14,
		1, 15, 1, 15, 1, 16, 1, 16, 0, 0, 17, 1, 1, 3, 2, 5, 3, 7, 4, 9, 5, 11,
		6, 13, 7, 15, 8, 17, 9, 19, 10, 21, 11, 23, 12, 25, 13, 27, 14, 29, 15,
		31, 16, 33, 17, 1, 0, 3, 2, 0, 65, 90, 97, 122, 1, 0, 48, 57, 2, 0, 9,
		9, 32, 32, 101, 0, 1, 1, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0,
		7, 1, 0, 0, 0, 0, 9, 1, 0, 0, 0, 0, 11, 1, 0, 0, 0, 0, 13, 1, 0, 0, 0,
		0, 15, 1, 0, 0, 0, 0, 17, 1, 0, 0, 0, 0, 19, 1, 0, 0, 0, 0, 21, 1, 0, 0,
		0, 0, 23, 1, 0, 0, 0, 0, 25, 1, 0, 0, 0, 0, 27, 1, 0, 0, 0, 0, 29, 1, 0,
		0, 0, 0, 31, 1, 0, 0, 0, 0, 33, 1, 0, 0, 0, 1, 35, 1, 0, 0, 0, 3, 37, 1,
		0, 0, 0, 5, 39, 1, 0, 0, 0, 7, 41, 1, 0, 0, 0, 9, 43, 1, 0, 0, 0, 11, 45,
		1, 0, 0, 0, 13, 47, 1, 0, 0, 0, 15, 50, 1, 0, 0, 0, 17, 55, 1, 0, 0, 0,
		19, 60, 1, 0, 0, 0, 21, 74, 1, 0, 0, 0, 23, 79, 1, 0, 0, 0, 25, 85, 1,
		0, 0, 0, 27, 87, 1, 0, 0, 0, 29, 89, 1, 0, 0, 0, 31, 91, 1, 0, 0, 0, 33,
		93, 1, 0, 0, 0, 35, 36, 5, 61, 0, 0, 36, 2, 1, 0, 0, 0, 37, 38, 5, 40,
		0, 0, 38, 4, 1, 0, 0, 0, 39, 40, 5, 41, 0, 0, 40, 6, 1, 0, 0, 0, 41, 42,
		5, 123, 0, 0, 42, 8, 1, 0, 0, 0, 43, 44, 5, 44, 0, 0, 44, 10, 1, 0, 0,
		0, 45, 46, 5, 125, 0, 0, 46, 12, 1, 0, 0, 0, 47, 48, 5, 58, 0, 0, 48, 14,
		1, 0, 0, 0, 49, 51, 7, 0, 0, 0, 50, 49, 1, 0, 0, 0, 51, 52, 1, 0, 0, 0,
		52, 50, 1, 0, 0, 0, 52, 53, 1, 0, 0, 0, 53, 16, 1, 0, 0, 0, 54, 56, 7,
		1, 0, 0, 55, 54, 1, 0, 0, 0, 56, 57, 1, 0, 0, 0, 57, 55, 1, 0, 0, 0, 57,
		58, 1, 0, 0, 0, 58, 18, 1, 0, 0, 0, 59, 61, 7, 1, 0, 0, 60, 59, 1, 0, 0,
		0, 61, 62, 1, 0, 0, 0, 62, 60, 1, 0, 0, 0, 62, 63, 1, 0, 0, 0, 63, 71,
		1, 0, 0, 0, 64, 68, 5, 46, 0, 0, 65, 67, 7, 1, 0, 0, 66, 65, 1, 0, 0, 0,
		67, 70, 1, 0, 0, 0, 68, 66, 1, 0, 0, 0, 68, 69, 1, 0, 0, 0, 69, 72, 1,
		0, 0, 0, 70, 68, 1, 0, 0, 0, 71, 64, 1, 0, 0, 0, 71, 72, 1, 0, 0, 0, 72,
		20, 1, 0, 0, 0, 73, 75, 5, 13, 0, 0, 74, 73, 1, 0, 0, 0, 74, 75, 1, 0,
		0, 0, 75, 76, 1, 0, 0, 0, 76, 77, 5, 10, 0, 0, 77, 22, 1, 0, 0, 0, 78,
		80, 7, 2, 0, 0, 79, 78, 1, 0, 0, 0, 80, 81, 1, 0, 0, 0, 81, 79, 1, 0, 0,
		0, 81, 82, 1, 0, 0, 0, 82, 83, 1, 0, 0, 0, 83, 84, 6, 11, 0, 0, 84, 24,
		1, 0, 0, 0, 85, 86, 5, 42, 0, 0, 86, 26, 1, 0, 0, 0, 87, 88, 5, 47, 0,
		0, 88, 28, 1, 0, 0, 0, 89, 90, 5, 43, 0, 0, 90, 30, 1, 0, 0, 0, 91, 92,
		5, 45, 0, 0, 92, 32, 1, 0, 0, 0, 93, 94, 5, 124, 0, 0, 94, 34, 1, 0, 0,
		0, 8, 0, 52, 57, 62, 68, 71, 74, 81, 1, 6, 0, 0,
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

// ProbabilityDistributionsLexerInit initializes any static state used to implement ProbabilityDistributionsLexer. By default the
// static state used to implement the lexer is lazily initialized during the first call to
// NewProbabilityDistributionsLexer(). You can call this function if you wish to initialize the static state ahead
// of time.
func ProbabilityDistributionsLexerInit() {
	staticData := &ProbabilityDistributionsLexerLexerStaticData
	staticData.once.Do(probabilitydistributionslexerLexerInit)
}

// NewProbabilityDistributionsLexer produces a new lexer instance for the optional input antlr.CharStream.
func NewProbabilityDistributionsLexer(input antlr.CharStream) *ProbabilityDistributionsLexer {
	ProbabilityDistributionsLexerInit()
	l := new(ProbabilityDistributionsLexer)
	l.BaseLexer = antlr.NewBaseLexer(input)
	staticData := &ProbabilityDistributionsLexerLexerStaticData
	l.Interpreter = antlr.NewLexerATNSimulator(l, staticData.atn, staticData.decisionToDFA, staticData.PredictionContextCache)
	l.channelNames = staticData.ChannelNames
	l.modeNames = staticData.ModeNames
	l.RuleNames = staticData.RuleNames
	l.LiteralNames = staticData.LiteralNames
	l.SymbolicNames = staticData.SymbolicNames
	l.GrammarFileName = "ProbabilityDistributions.g4"
	// TODO: l.EOF = antlr.TokenEOF

	return l
}

// ProbabilityDistributionsLexer tokens.
const (
	ProbabilityDistributionsLexerT__0    = 1
	ProbabilityDistributionsLexerT__1    = 2
	ProbabilityDistributionsLexerT__2    = 3
	ProbabilityDistributionsLexerT__3    = 4
	ProbabilityDistributionsLexerT__4    = 5
	ProbabilityDistributionsLexerT__5    = 6
	ProbabilityDistributionsLexerT__6    = 7
	ProbabilityDistributionsLexerID      = 8
	ProbabilityDistributionsLexerINT     = 9
	ProbabilityDistributionsLexerFLOAT   = 10
	ProbabilityDistributionsLexerNEWLINE = 11
	ProbabilityDistributionsLexerWS      = 12
	ProbabilityDistributionsLexerMUL     = 13
	ProbabilityDistributionsLexerDIV     = 14
	ProbabilityDistributionsLexerADD     = 15
	ProbabilityDistributionsLexerSUB     = 16
	ProbabilityDistributionsLexerOR      = 17
)
