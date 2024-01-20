// Code generated from Cymbol.g4 by ANTLR 4.13.1. DO NOT EDIT.

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

type CymbolLexer struct {
	*antlr.BaseLexer
	channelNames []string
	modeNames    []string
	// TODO: EOF string
}

var CymbolLexerLexerStaticData struct {
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

func cymbollexerLexerInit() {
	staticData := &CymbolLexerLexerStaticData
	staticData.ChannelNames = []string{
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN",
	}
	staticData.ModeNames = []string{
		"DEFAULT_MODE",
	}
	staticData.LiteralNames = []string{
		"", "'='", "';'", "'float'", "'int'", "'void'", "'('", "')'", "','",
		"'{'", "'}'", "'if'", "'then'", "'else'", "'return'", "'['", "']'",
		"'-'", "'!'", "'*'", "'+'", "'=='",
	}
	staticData.SymbolicNames = []string{
		"", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
		"", "", "", "", "", "ID", "INT", "WS", "SL_COMMENT",
	}
	staticData.RuleNames = []string{
		"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8",
		"T__9", "T__10", "T__11", "T__12", "T__13", "T__14", "T__15", "T__16",
		"T__17", "T__18", "T__19", "T__20", "ID", "LETTER", "INT", "WS", "SL_COMMENT",
	}
	staticData.PredictionContextCache = antlr.NewPredictionContextCache()
	staticData.serializedATN = []int32{
		4, 0, 25, 152, 6, -1, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2,
		4, 7, 4, 2, 5, 7, 5, 2, 6, 7, 6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2,
		10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13, 2, 14, 7, 14, 2, 15,
		7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20, 7,
		20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25,
		1, 0, 1, 0, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 1, 3,
		1, 3, 1, 3, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 5, 1, 5, 1, 6, 1, 6, 1, 7,
		1, 7, 1, 8, 1, 8, 1, 9, 1, 9, 1, 10, 1, 10, 1, 10, 1, 11, 1, 11, 1, 11,
		1, 11, 1, 11, 1, 12, 1, 12, 1, 12, 1, 12, 1, 12, 1, 13, 1, 13, 1, 13, 1,
		13, 1, 13, 1, 13, 1, 13, 1, 14, 1, 14, 1, 15, 1, 15, 1, 16, 1, 16, 1, 17,
		1, 17, 1, 18, 1, 18, 1, 19, 1, 19, 1, 20, 1, 20, 1, 20, 1, 21, 1, 21, 1,
		21, 5, 21, 121, 8, 21, 10, 21, 12, 21, 124, 9, 21, 1, 22, 1, 22, 1, 23,
		4, 23, 129, 8, 23, 11, 23, 12, 23, 130, 1, 24, 4, 24, 134, 8, 24, 11, 24,
		12, 24, 135, 1, 24, 1, 24, 1, 25, 1, 25, 1, 25, 1, 25, 5, 25, 144, 8, 25,
		10, 25, 12, 25, 147, 9, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 145, 0, 26,
		1, 1, 3, 2, 5, 3, 7, 4, 9, 5, 11, 6, 13, 7, 15, 8, 17, 9, 19, 10, 21, 11,
		23, 12, 25, 13, 27, 14, 29, 15, 31, 16, 33, 17, 35, 18, 37, 19, 39, 20,
		41, 21, 43, 22, 45, 0, 47, 23, 49, 24, 51, 25, 1, 0, 3, 1, 0, 48, 57, 2,
		0, 65, 90, 97, 122, 3, 0, 9, 10, 13, 13, 32, 32, 155, 0, 1, 1, 0, 0, 0,
		0, 3, 1, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 7, 1, 0, 0, 0, 0, 9, 1, 0, 0, 0,
		0, 11, 1, 0, 0, 0, 0, 13, 1, 0, 0, 0, 0, 15, 1, 0, 0, 0, 0, 17, 1, 0, 0,
		0, 0, 19, 1, 0, 0, 0, 0, 21, 1, 0, 0, 0, 0, 23, 1, 0, 0, 0, 0, 25, 1, 0,
		0, 0, 0, 27, 1, 0, 0, 0, 0, 29, 1, 0, 0, 0, 0, 31, 1, 0, 0, 0, 0, 33, 1,
		0, 0, 0, 0, 35, 1, 0, 0, 0, 0, 37, 1, 0, 0, 0, 0, 39, 1, 0, 0, 0, 0, 41,
		1, 0, 0, 0, 0, 43, 1, 0, 0, 0, 0, 47, 1, 0, 0, 0, 0, 49, 1, 0, 0, 0, 0,
		51, 1, 0, 0, 0, 1, 53, 1, 0, 0, 0, 3, 55, 1, 0, 0, 0, 5, 57, 1, 0, 0, 0,
		7, 63, 1, 0, 0, 0, 9, 67, 1, 0, 0, 0, 11, 72, 1, 0, 0, 0, 13, 74, 1, 0,
		0, 0, 15, 76, 1, 0, 0, 0, 17, 78, 1, 0, 0, 0, 19, 80, 1, 0, 0, 0, 21, 82,
		1, 0, 0, 0, 23, 85, 1, 0, 0, 0, 25, 90, 1, 0, 0, 0, 27, 95, 1, 0, 0, 0,
		29, 102, 1, 0, 0, 0, 31, 104, 1, 0, 0, 0, 33, 106, 1, 0, 0, 0, 35, 108,
		1, 0, 0, 0, 37, 110, 1, 0, 0, 0, 39, 112, 1, 0, 0, 0, 41, 114, 1, 0, 0,
		0, 43, 117, 1, 0, 0, 0, 45, 125, 1, 0, 0, 0, 47, 128, 1, 0, 0, 0, 49, 133,
		1, 0, 0, 0, 51, 139, 1, 0, 0, 0, 53, 54, 5, 61, 0, 0, 54, 2, 1, 0, 0, 0,
		55, 56, 5, 59, 0, 0, 56, 4, 1, 0, 0, 0, 57, 58, 5, 102, 0, 0, 58, 59, 5,
		108, 0, 0, 59, 60, 5, 111, 0, 0, 60, 61, 5, 97, 0, 0, 61, 62, 5, 116, 0,
		0, 62, 6, 1, 0, 0, 0, 63, 64, 5, 105, 0, 0, 64, 65, 5, 110, 0, 0, 65, 66,
		5, 116, 0, 0, 66, 8, 1, 0, 0, 0, 67, 68, 5, 118, 0, 0, 68, 69, 5, 111,
		0, 0, 69, 70, 5, 105, 0, 0, 70, 71, 5, 100, 0, 0, 71, 10, 1, 0, 0, 0, 72,
		73, 5, 40, 0, 0, 73, 12, 1, 0, 0, 0, 74, 75, 5, 41, 0, 0, 75, 14, 1, 0,
		0, 0, 76, 77, 5, 44, 0, 0, 77, 16, 1, 0, 0, 0, 78, 79, 5, 123, 0, 0, 79,
		18, 1, 0, 0, 0, 80, 81, 5, 125, 0, 0, 81, 20, 1, 0, 0, 0, 82, 83, 5, 105,
		0, 0, 83, 84, 5, 102, 0, 0, 84, 22, 1, 0, 0, 0, 85, 86, 5, 116, 0, 0, 86,
		87, 5, 104, 0, 0, 87, 88, 5, 101, 0, 0, 88, 89, 5, 110, 0, 0, 89, 24, 1,
		0, 0, 0, 90, 91, 5, 101, 0, 0, 91, 92, 5, 108, 0, 0, 92, 93, 5, 115, 0,
		0, 93, 94, 5, 101, 0, 0, 94, 26, 1, 0, 0, 0, 95, 96, 5, 114, 0, 0, 96,
		97, 5, 101, 0, 0, 97, 98, 5, 116, 0, 0, 98, 99, 5, 117, 0, 0, 99, 100,
		5, 114, 0, 0, 100, 101, 5, 110, 0, 0, 101, 28, 1, 0, 0, 0, 102, 103, 5,
		91, 0, 0, 103, 30, 1, 0, 0, 0, 104, 105, 5, 93, 0, 0, 105, 32, 1, 0, 0,
		0, 106, 107, 5, 45, 0, 0, 107, 34, 1, 0, 0, 0, 108, 109, 5, 33, 0, 0, 109,
		36, 1, 0, 0, 0, 110, 111, 5, 42, 0, 0, 111, 38, 1, 0, 0, 0, 112, 113, 5,
		43, 0, 0, 113, 40, 1, 0, 0, 0, 114, 115, 5, 61, 0, 0, 115, 116, 5, 61,
		0, 0, 116, 42, 1, 0, 0, 0, 117, 122, 3, 45, 22, 0, 118, 121, 3, 45, 22,
		0, 119, 121, 7, 0, 0, 0, 120, 118, 1, 0, 0, 0, 120, 119, 1, 0, 0, 0, 121,
		124, 1, 0, 0, 0, 122, 120, 1, 0, 0, 0, 122, 123, 1, 0, 0, 0, 123, 44, 1,
		0, 0, 0, 124, 122, 1, 0, 0, 0, 125, 126, 7, 1, 0, 0, 126, 46, 1, 0, 0,
		0, 127, 129, 7, 0, 0, 0, 128, 127, 1, 0, 0, 0, 129, 130, 1, 0, 0, 0, 130,
		128, 1, 0, 0, 0, 130, 131, 1, 0, 0, 0, 131, 48, 1, 0, 0, 0, 132, 134, 7,
		2, 0, 0, 133, 132, 1, 0, 0, 0, 134, 135, 1, 0, 0, 0, 135, 133, 1, 0, 0,
		0, 135, 136, 1, 0, 0, 0, 136, 137, 1, 0, 0, 0, 137, 138, 6, 24, 0, 0, 138,
		50, 1, 0, 0, 0, 139, 140, 5, 47, 0, 0, 140, 141, 5, 47, 0, 0, 141, 145,
		1, 0, 0, 0, 142, 144, 9, 0, 0, 0, 143, 142, 1, 0, 0, 0, 144, 147, 1, 0,
		0, 0, 145, 146, 1, 0, 0, 0, 145, 143, 1, 0, 0, 0, 146, 148, 1, 0, 0, 0,
		147, 145, 1, 0, 0, 0, 148, 149, 5, 10, 0, 0, 149, 150, 1, 0, 0, 0, 150,
		151, 6, 25, 0, 0, 151, 52, 1, 0, 0, 0, 6, 0, 120, 122, 130, 135, 145, 1,
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

// CymbolLexerInit initializes any static state used to implement CymbolLexer. By default the
// static state used to implement the lexer is lazily initialized during the first call to
// NewCymbolLexer(). You can call this function if you wish to initialize the static state ahead
// of time.
func CymbolLexerInit() {
	staticData := &CymbolLexerLexerStaticData
	staticData.once.Do(cymbollexerLexerInit)
}

// NewCymbolLexer produces a new lexer instance for the optional input antlr.CharStream.
func NewCymbolLexer(input antlr.CharStream) *CymbolLexer {
	CymbolLexerInit()
	l := new(CymbolLexer)
	l.BaseLexer = antlr.NewBaseLexer(input)
	staticData := &CymbolLexerLexerStaticData
	l.Interpreter = antlr.NewLexerATNSimulator(l, staticData.atn, staticData.decisionToDFA, staticData.PredictionContextCache)
	l.channelNames = staticData.ChannelNames
	l.modeNames = staticData.ModeNames
	l.RuleNames = staticData.RuleNames
	l.LiteralNames = staticData.LiteralNames
	l.SymbolicNames = staticData.SymbolicNames
	l.GrammarFileName = "Cymbol.g4"
	// TODO: l.EOF = antlr.TokenEOF

	return l
}

// CymbolLexer tokens.
const (
	CymbolLexerT__0       = 1
	CymbolLexerT__1       = 2
	CymbolLexerT__2       = 3
	CymbolLexerT__3       = 4
	CymbolLexerT__4       = 5
	CymbolLexerT__5       = 6
	CymbolLexerT__6       = 7
	CymbolLexerT__7       = 8
	CymbolLexerT__8       = 9
	CymbolLexerT__9       = 10
	CymbolLexerT__10      = 11
	CymbolLexerT__11      = 12
	CymbolLexerT__12      = 13
	CymbolLexerT__13      = 14
	CymbolLexerT__14      = 15
	CymbolLexerT__15      = 16
	CymbolLexerT__16      = 17
	CymbolLexerT__17      = 18
	CymbolLexerT__18      = 19
	CymbolLexerT__19      = 20
	CymbolLexerT__20      = 21
	CymbolLexerID         = 22
	CymbolLexerINT        = 23
	CymbolLexerWS         = 24
	CymbolLexerSL_COMMENT = 25
)
