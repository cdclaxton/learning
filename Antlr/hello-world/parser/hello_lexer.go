// Code generated from Hello.g4 by ANTLR 4.13.1. DO NOT EDIT.

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

type HelloLexer struct {
	*antlr.BaseLexer
	channelNames []string
	modeNames    []string
	// TODO: EOF string
}

var HelloLexerLexerStaticData struct {
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

func hellolexerLexerInit() {
	staticData := &HelloLexerLexerStaticData
	staticData.ChannelNames = []string{
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN",
	}
	staticData.ModeNames = []string{
		"DEFAULT_MODE",
	}
	staticData.LiteralNames = []string{
		"", "'hello'",
	}
	staticData.SymbolicNames = []string{
		"", "", "ID", "WS",
	}
	staticData.RuleNames = []string{
		"T__0", "ID", "WS",
	}
	staticData.PredictionContextCache = antlr.NewPredictionContextCache()
	staticData.serializedATN = []int32{
		4, 0, 3, 25, 6, -1, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 1, 0, 1, 0, 1,
		0, 1, 0, 1, 0, 1, 0, 1, 1, 4, 1, 15, 8, 1, 11, 1, 12, 1, 16, 1, 2, 4, 2,
		20, 8, 2, 11, 2, 12, 2, 21, 1, 2, 1, 2, 0, 0, 3, 1, 1, 3, 2, 5, 3, 1, 0,
		2, 1, 0, 97, 122, 3, 0, 9, 10, 13, 13, 32, 32, 26, 0, 1, 1, 0, 0, 0, 0,
		3, 1, 0, 0, 0, 0, 5, 1, 0, 0, 0, 1, 7, 1, 0, 0, 0, 3, 14, 1, 0, 0, 0, 5,
		19, 1, 0, 0, 0, 7, 8, 5, 104, 0, 0, 8, 9, 5, 101, 0, 0, 9, 10, 5, 108,
		0, 0, 10, 11, 5, 108, 0, 0, 11, 12, 5, 111, 0, 0, 12, 2, 1, 0, 0, 0, 13,
		15, 7, 0, 0, 0, 14, 13, 1, 0, 0, 0, 15, 16, 1, 0, 0, 0, 16, 14, 1, 0, 0,
		0, 16, 17, 1, 0, 0, 0, 17, 4, 1, 0, 0, 0, 18, 20, 7, 1, 0, 0, 19, 18, 1,
		0, 0, 0, 20, 21, 1, 0, 0, 0, 21, 19, 1, 0, 0, 0, 21, 22, 1, 0, 0, 0, 22,
		23, 1, 0, 0, 0, 23, 24, 6, 2, 0, 0, 24, 6, 1, 0, 0, 0, 3, 0, 16, 21, 1,
		6, 0, 0,
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

// HelloLexerInit initializes any static state used to implement HelloLexer. By default the
// static state used to implement the lexer is lazily initialized during the first call to
// NewHelloLexer(). You can call this function if you wish to initialize the static state ahead
// of time.
func HelloLexerInit() {
	staticData := &HelloLexerLexerStaticData
	staticData.once.Do(hellolexerLexerInit)
}

// NewHelloLexer produces a new lexer instance for the optional input antlr.CharStream.
func NewHelloLexer(input antlr.CharStream) *HelloLexer {
	HelloLexerInit()
	l := new(HelloLexer)
	l.BaseLexer = antlr.NewBaseLexer(input)
	staticData := &HelloLexerLexerStaticData
	l.Interpreter = antlr.NewLexerATNSimulator(l, staticData.atn, staticData.decisionToDFA, staticData.PredictionContextCache)
	l.channelNames = staticData.ChannelNames
	l.modeNames = staticData.ModeNames
	l.RuleNames = staticData.RuleNames
	l.LiteralNames = staticData.LiteralNames
	l.SymbolicNames = staticData.SymbolicNames
	l.GrammarFileName = "Hello.g4"
	// TODO: l.EOF = antlr.TokenEOF

	return l
}

// HelloLexer tokens.
const (
	HelloLexerT__0 = 1
	HelloLexerID   = 2
	HelloLexerWS   = 3
)
