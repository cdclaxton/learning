// Code generated from Hello.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // Hello

import (
	"fmt"
	"strconv"
	"sync"

	"github.com/antlr4-go/antlr/v4"
)

// Suppress unused import errors
var _ = fmt.Printf
var _ = strconv.Itoa
var _ = sync.Once{}

type HelloParser struct {
	*antlr.BaseParser
}

var HelloParserStaticData struct {
	once                   sync.Once
	serializedATN          []int32
	LiteralNames           []string
	SymbolicNames          []string
	RuleNames              []string
	PredictionContextCache *antlr.PredictionContextCache
	atn                    *antlr.ATN
	decisionToDFA          []*antlr.DFA
}

func helloParserInit() {
	staticData := &HelloParserStaticData
	staticData.LiteralNames = []string{
		"", "'hello'",
	}
	staticData.SymbolicNames = []string{
		"", "", "ID", "WS",
	}
	staticData.RuleNames = []string{
		"r",
	}
	staticData.PredictionContextCache = antlr.NewPredictionContextCache()
	staticData.serializedATN = []int32{
		4, 1, 3, 6, 2, 0, 7, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 4, 0,
		2, 1, 0, 0, 0, 2, 3, 5, 1, 0, 0, 3, 4, 5, 2, 0, 0, 4, 1, 1, 0, 0, 0, 0,
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

// HelloParserInit initializes any static state used to implement HelloParser. By default the
// static state used to implement the parser is lazily initialized during the first call to
// NewHelloParser(). You can call this function if you wish to initialize the static state ahead
// of time.
func HelloParserInit() {
	staticData := &HelloParserStaticData
	staticData.once.Do(helloParserInit)
}

// NewHelloParser produces a new parser instance for the optional input antlr.TokenStream.
func NewHelloParser(input antlr.TokenStream) *HelloParser {
	HelloParserInit()
	this := new(HelloParser)
	this.BaseParser = antlr.NewBaseParser(input)
	staticData := &HelloParserStaticData
	this.Interpreter = antlr.NewParserATNSimulator(this, staticData.atn, staticData.decisionToDFA, staticData.PredictionContextCache)
	this.RuleNames = staticData.RuleNames
	this.LiteralNames = staticData.LiteralNames
	this.SymbolicNames = staticData.SymbolicNames
	this.GrammarFileName = "Hello.g4"

	return this
}

// HelloParser tokens.
const (
	HelloParserEOF  = antlr.TokenEOF
	HelloParserT__0 = 1
	HelloParserID   = 2
	HelloParserWS   = 3
)

// HelloParserRULE_r is the HelloParser rule.
const HelloParserRULE_r = 0

// IRContext is an interface to support dynamic dispatch.
type IRContext interface {
	antlr.ParserRuleContext

	// GetParser returns the parser.
	GetParser() antlr.Parser

	// Getter signatures
	ID() antlr.TerminalNode

	// IsRContext differentiates from other interfaces.
	IsRContext()
}

type RContext struct {
	antlr.BaseParserRuleContext
	parser antlr.Parser
}

func NewEmptyRContext() *RContext {
	var p = new(RContext)
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = HelloParserRULE_r
	return p
}

func InitEmptyRContext(p *RContext) {
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = HelloParserRULE_r
}

func (*RContext) IsRContext() {}

func NewRContext(parser antlr.Parser, parent antlr.ParserRuleContext, invokingState int) *RContext {
	var p = new(RContext)

	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, parent, invokingState)

	p.parser = parser
	p.RuleIndex = HelloParserRULE_r

	return p
}

func (s *RContext) GetParser() antlr.Parser { return s.parser }

func (s *RContext) ID() antlr.TerminalNode {
	return s.GetToken(HelloParserID, 0)
}

func (s *RContext) GetRuleContext() antlr.RuleContext {
	return s
}

func (s *RContext) ToStringTree(ruleNames []string, recog antlr.Recognizer) string {
	return antlr.TreesStringTree(s, ruleNames, recog)
}

func (s *RContext) EnterRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(HelloListener); ok {
		listenerT.EnterR(s)
	}
}

func (s *RContext) ExitRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(HelloListener); ok {
		listenerT.ExitR(s)
	}
}

func (p *HelloParser) R() (localctx IRContext) {
	localctx = NewRContext(p, p.GetParserRuleContext(), p.GetState())
	p.EnterRule(localctx, 0, HelloParserRULE_r)
	p.EnterOuterAlt(localctx, 1)
	{
		p.SetState(2)
		p.Match(HelloParserT__0)
		if p.HasError() {
			// Recognition error - abort rule
			goto errorExit
		}
	}
	{
		p.SetState(3)
		p.Match(HelloParserID)
		if p.HasError() {
			// Recognition error - abort rule
			goto errorExit
		}
	}

errorExit:
	if p.HasError() {
		v := p.GetError()
		localctx.SetException(v)
		p.GetErrorHandler().ReportError(p, v)
		p.GetErrorHandler().Recover(p, v)
		p.SetError(nil)
	}
	p.ExitRule()
	return localctx
	goto errorExit // Trick to prevent compiler error if the label is not used
}
