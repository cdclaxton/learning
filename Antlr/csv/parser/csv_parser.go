// Code generated from Csv.g4 by ANTLR 4.13.1. DO NOT EDIT.

package parser // Csv

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

type CsvParser struct {
	*antlr.BaseParser
}

var CsvParserStaticData struct {
	once                   sync.Once
	serializedATN          []int32
	LiteralNames           []string
	SymbolicNames          []string
	RuleNames              []string
	PredictionContextCache *antlr.PredictionContextCache
	atn                    *antlr.ATN
	decisionToDFA          []*antlr.DFA
}

func csvParserInit() {
	staticData := &CsvParserStaticData
	staticData.LiteralNames = []string{
		"", "','", "'\\r'", "'\\n'",
	}
	staticData.SymbolicNames = []string{
		"", "", "", "", "TEXT", "STRING",
	}
	staticData.RuleNames = []string{
		"file", "hdr", "row", "field",
	}
	staticData.PredictionContextCache = antlr.NewPredictionContextCache()
	staticData.serializedATN = []int32{
		4, 1, 5, 35, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 1, 0, 1, 0,
		4, 0, 11, 8, 0, 11, 0, 12, 0, 12, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 5, 2, 20,
		8, 2, 10, 2, 12, 2, 23, 9, 2, 1, 2, 3, 2, 26, 8, 2, 1, 2, 1, 2, 1, 3, 1,
		3, 1, 3, 3, 3, 33, 8, 3, 1, 3, 0, 0, 4, 0, 2, 4, 6, 0, 0, 35, 0, 8, 1,
		0, 0, 0, 2, 14, 1, 0, 0, 0, 4, 16, 1, 0, 0, 0, 6, 32, 1, 0, 0, 0, 8, 10,
		3, 2, 1, 0, 9, 11, 3, 4, 2, 0, 10, 9, 1, 0, 0, 0, 11, 12, 1, 0, 0, 0, 12,
		10, 1, 0, 0, 0, 12, 13, 1, 0, 0, 0, 13, 1, 1, 0, 0, 0, 14, 15, 3, 4, 2,
		0, 15, 3, 1, 0, 0, 0, 16, 21, 3, 6, 3, 0, 17, 18, 5, 1, 0, 0, 18, 20, 3,
		6, 3, 0, 19, 17, 1, 0, 0, 0, 20, 23, 1, 0, 0, 0, 21, 19, 1, 0, 0, 0, 21,
		22, 1, 0, 0, 0, 22, 25, 1, 0, 0, 0, 23, 21, 1, 0, 0, 0, 24, 26, 5, 2, 0,
		0, 25, 24, 1, 0, 0, 0, 25, 26, 1, 0, 0, 0, 26, 27, 1, 0, 0, 0, 27, 28,
		5, 3, 0, 0, 28, 5, 1, 0, 0, 0, 29, 33, 5, 4, 0, 0, 30, 33, 5, 5, 0, 0,
		31, 33, 1, 0, 0, 0, 32, 29, 1, 0, 0, 0, 32, 30, 1, 0, 0, 0, 32, 31, 1,
		0, 0, 0, 33, 7, 1, 0, 0, 0, 4, 12, 21, 25, 32,
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

// CsvParserInit initializes any static state used to implement CsvParser. By default the
// static state used to implement the parser is lazily initialized during the first call to
// NewCsvParser(). You can call this function if you wish to initialize the static state ahead
// of time.
func CsvParserInit() {
	staticData := &CsvParserStaticData
	staticData.once.Do(csvParserInit)
}

// NewCsvParser produces a new parser instance for the optional input antlr.TokenStream.
func NewCsvParser(input antlr.TokenStream) *CsvParser {
	CsvParserInit()
	this := new(CsvParser)
	this.BaseParser = antlr.NewBaseParser(input)
	staticData := &CsvParserStaticData
	this.Interpreter = antlr.NewParserATNSimulator(this, staticData.atn, staticData.decisionToDFA, staticData.PredictionContextCache)
	this.RuleNames = staticData.RuleNames
	this.LiteralNames = staticData.LiteralNames
	this.SymbolicNames = staticData.SymbolicNames
	this.GrammarFileName = "Csv.g4"

	return this
}

// CsvParser tokens.
const (
	CsvParserEOF    = antlr.TokenEOF
	CsvParserT__0   = 1
	CsvParserT__1   = 2
	CsvParserT__2   = 3
	CsvParserTEXT   = 4
	CsvParserSTRING = 5
)

// CsvParser rules.
const (
	CsvParserRULE_file  = 0
	CsvParserRULE_hdr   = 1
	CsvParserRULE_row   = 2
	CsvParserRULE_field = 3
)

// IFileContext is an interface to support dynamic dispatch.
type IFileContext interface {
	antlr.ParserRuleContext

	// GetParser returns the parser.
	GetParser() antlr.Parser

	// Getter signatures
	Hdr() IHdrContext
	AllRow() []IRowContext
	Row(i int) IRowContext

	// IsFileContext differentiates from other interfaces.
	IsFileContext()
}

type FileContext struct {
	antlr.BaseParserRuleContext
	parser antlr.Parser
}

func NewEmptyFileContext() *FileContext {
	var p = new(FileContext)
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = CsvParserRULE_file
	return p
}

func InitEmptyFileContext(p *FileContext) {
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = CsvParserRULE_file
}

func (*FileContext) IsFileContext() {}

func NewFileContext(parser antlr.Parser, parent antlr.ParserRuleContext, invokingState int) *FileContext {
	var p = new(FileContext)

	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, parent, invokingState)

	p.parser = parser
	p.RuleIndex = CsvParserRULE_file

	return p
}

func (s *FileContext) GetParser() antlr.Parser { return s.parser }

func (s *FileContext) Hdr() IHdrContext {
	var t antlr.RuleContext
	for _, ctx := range s.GetChildren() {
		if _, ok := ctx.(IHdrContext); ok {
			t = ctx.(antlr.RuleContext)
			break
		}
	}

	if t == nil {
		return nil
	}

	return t.(IHdrContext)
}

func (s *FileContext) AllRow() []IRowContext {
	children := s.GetChildren()
	len := 0
	for _, ctx := range children {
		if _, ok := ctx.(IRowContext); ok {
			len++
		}
	}

	tst := make([]IRowContext, len)
	i := 0
	for _, ctx := range children {
		if t, ok := ctx.(IRowContext); ok {
			tst[i] = t.(IRowContext)
			i++
		}
	}

	return tst
}

func (s *FileContext) Row(i int) IRowContext {
	var t antlr.RuleContext
	j := 0
	for _, ctx := range s.GetChildren() {
		if _, ok := ctx.(IRowContext); ok {
			if j == i {
				t = ctx.(antlr.RuleContext)
				break
			}
			j++
		}
	}

	if t == nil {
		return nil
	}

	return t.(IRowContext)
}

func (s *FileContext) GetRuleContext() antlr.RuleContext {
	return s
}

func (s *FileContext) ToStringTree(ruleNames []string, recog antlr.Recognizer) string {
	return antlr.TreesStringTree(s, ruleNames, recog)
}

func (s *FileContext) EnterRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(CsvListener); ok {
		listenerT.EnterFile(s)
	}
}

func (s *FileContext) ExitRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(CsvListener); ok {
		listenerT.ExitFile(s)
	}
}

func (p *CsvParser) File() (localctx IFileContext) {
	localctx = NewFileContext(p, p.GetParserRuleContext(), p.GetState())
	p.EnterRule(localctx, 0, CsvParserRULE_file)
	var _la int

	p.EnterOuterAlt(localctx, 1)
	{
		p.SetState(8)
		p.Hdr()
	}
	p.SetState(10)
	p.GetErrorHandler().Sync(p)
	if p.HasError() {
		goto errorExit
	}
	_la = p.GetTokenStream().LA(1)

	for ok := true; ok; ok = ((int64(_la) & ^0x3f) == 0 && ((int64(1)<<_la)&62) != 0) {
		{
			p.SetState(9)
			p.Row()
		}

		p.SetState(12)
		p.GetErrorHandler().Sync(p)
		if p.HasError() {
			goto errorExit
		}
		_la = p.GetTokenStream().LA(1)
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

// IHdrContext is an interface to support dynamic dispatch.
type IHdrContext interface {
	antlr.ParserRuleContext

	// GetParser returns the parser.
	GetParser() antlr.Parser

	// Getter signatures
	Row() IRowContext

	// IsHdrContext differentiates from other interfaces.
	IsHdrContext()
}

type HdrContext struct {
	antlr.BaseParserRuleContext
	parser antlr.Parser
}

func NewEmptyHdrContext() *HdrContext {
	var p = new(HdrContext)
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = CsvParserRULE_hdr
	return p
}

func InitEmptyHdrContext(p *HdrContext) {
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = CsvParserRULE_hdr
}

func (*HdrContext) IsHdrContext() {}

func NewHdrContext(parser antlr.Parser, parent antlr.ParserRuleContext, invokingState int) *HdrContext {
	var p = new(HdrContext)

	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, parent, invokingState)

	p.parser = parser
	p.RuleIndex = CsvParserRULE_hdr

	return p
}

func (s *HdrContext) GetParser() antlr.Parser { return s.parser }

func (s *HdrContext) Row() IRowContext {
	var t antlr.RuleContext
	for _, ctx := range s.GetChildren() {
		if _, ok := ctx.(IRowContext); ok {
			t = ctx.(antlr.RuleContext)
			break
		}
	}

	if t == nil {
		return nil
	}

	return t.(IRowContext)
}

func (s *HdrContext) GetRuleContext() antlr.RuleContext {
	return s
}

func (s *HdrContext) ToStringTree(ruleNames []string, recog antlr.Recognizer) string {
	return antlr.TreesStringTree(s, ruleNames, recog)
}

func (s *HdrContext) EnterRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(CsvListener); ok {
		listenerT.EnterHdr(s)
	}
}

func (s *HdrContext) ExitRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(CsvListener); ok {
		listenerT.ExitHdr(s)
	}
}

func (p *CsvParser) Hdr() (localctx IHdrContext) {
	localctx = NewHdrContext(p, p.GetParserRuleContext(), p.GetState())
	p.EnterRule(localctx, 2, CsvParserRULE_hdr)
	p.EnterOuterAlt(localctx, 1)
	{
		p.SetState(14)
		p.Row()
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

// IRowContext is an interface to support dynamic dispatch.
type IRowContext interface {
	antlr.ParserRuleContext

	// GetParser returns the parser.
	GetParser() antlr.Parser

	// Getter signatures
	AllField() []IFieldContext
	Field(i int) IFieldContext

	// IsRowContext differentiates from other interfaces.
	IsRowContext()
}

type RowContext struct {
	antlr.BaseParserRuleContext
	parser antlr.Parser
}

func NewEmptyRowContext() *RowContext {
	var p = new(RowContext)
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = CsvParserRULE_row
	return p
}

func InitEmptyRowContext(p *RowContext) {
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = CsvParserRULE_row
}

func (*RowContext) IsRowContext() {}

func NewRowContext(parser antlr.Parser, parent antlr.ParserRuleContext, invokingState int) *RowContext {
	var p = new(RowContext)

	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, parent, invokingState)

	p.parser = parser
	p.RuleIndex = CsvParserRULE_row

	return p
}

func (s *RowContext) GetParser() antlr.Parser { return s.parser }

func (s *RowContext) AllField() []IFieldContext {
	children := s.GetChildren()
	len := 0
	for _, ctx := range children {
		if _, ok := ctx.(IFieldContext); ok {
			len++
		}
	}

	tst := make([]IFieldContext, len)
	i := 0
	for _, ctx := range children {
		if t, ok := ctx.(IFieldContext); ok {
			tst[i] = t.(IFieldContext)
			i++
		}
	}

	return tst
}

func (s *RowContext) Field(i int) IFieldContext {
	var t antlr.RuleContext
	j := 0
	for _, ctx := range s.GetChildren() {
		if _, ok := ctx.(IFieldContext); ok {
			if j == i {
				t = ctx.(antlr.RuleContext)
				break
			}
			j++
		}
	}

	if t == nil {
		return nil
	}

	return t.(IFieldContext)
}

func (s *RowContext) GetRuleContext() antlr.RuleContext {
	return s
}

func (s *RowContext) ToStringTree(ruleNames []string, recog antlr.Recognizer) string {
	return antlr.TreesStringTree(s, ruleNames, recog)
}

func (s *RowContext) EnterRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(CsvListener); ok {
		listenerT.EnterRow(s)
	}
}

func (s *RowContext) ExitRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(CsvListener); ok {
		listenerT.ExitRow(s)
	}
}

func (p *CsvParser) Row() (localctx IRowContext) {
	localctx = NewRowContext(p, p.GetParserRuleContext(), p.GetState())
	p.EnterRule(localctx, 4, CsvParserRULE_row)
	var _la int

	p.EnterOuterAlt(localctx, 1)
	{
		p.SetState(16)
		p.Field()
	}
	p.SetState(21)
	p.GetErrorHandler().Sync(p)
	if p.HasError() {
		goto errorExit
	}
	_la = p.GetTokenStream().LA(1)

	for _la == CsvParserT__0 {
		{
			p.SetState(17)
			p.Match(CsvParserT__0)
			if p.HasError() {
				// Recognition error - abort rule
				goto errorExit
			}
		}
		{
			p.SetState(18)
			p.Field()
		}

		p.SetState(23)
		p.GetErrorHandler().Sync(p)
		if p.HasError() {
			goto errorExit
		}
		_la = p.GetTokenStream().LA(1)
	}
	p.SetState(25)
	p.GetErrorHandler().Sync(p)
	if p.HasError() {
		goto errorExit
	}
	_la = p.GetTokenStream().LA(1)

	if _la == CsvParserT__1 {
		{
			p.SetState(24)
			p.Match(CsvParserT__1)
			if p.HasError() {
				// Recognition error - abort rule
				goto errorExit
			}
		}

	}
	{
		p.SetState(27)
		p.Match(CsvParserT__2)
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

// IFieldContext is an interface to support dynamic dispatch.
type IFieldContext interface {
	antlr.ParserRuleContext

	// GetParser returns the parser.
	GetParser() antlr.Parser

	// Getter signatures
	TEXT() antlr.TerminalNode
	STRING() antlr.TerminalNode

	// IsFieldContext differentiates from other interfaces.
	IsFieldContext()
}

type FieldContext struct {
	antlr.BaseParserRuleContext
	parser antlr.Parser
}

func NewEmptyFieldContext() *FieldContext {
	var p = new(FieldContext)
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = CsvParserRULE_field
	return p
}

func InitEmptyFieldContext(p *FieldContext) {
	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, nil, -1)
	p.RuleIndex = CsvParserRULE_field
}

func (*FieldContext) IsFieldContext() {}

func NewFieldContext(parser antlr.Parser, parent antlr.ParserRuleContext, invokingState int) *FieldContext {
	var p = new(FieldContext)

	antlr.InitBaseParserRuleContext(&p.BaseParserRuleContext, parent, invokingState)

	p.parser = parser
	p.RuleIndex = CsvParserRULE_field

	return p
}

func (s *FieldContext) GetParser() antlr.Parser { return s.parser }

func (s *FieldContext) TEXT() antlr.TerminalNode {
	return s.GetToken(CsvParserTEXT, 0)
}

func (s *FieldContext) STRING() antlr.TerminalNode {
	return s.GetToken(CsvParserSTRING, 0)
}

func (s *FieldContext) GetRuleContext() antlr.RuleContext {
	return s
}

func (s *FieldContext) ToStringTree(ruleNames []string, recog antlr.Recognizer) string {
	return antlr.TreesStringTree(s, ruleNames, recog)
}

func (s *FieldContext) EnterRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(CsvListener); ok {
		listenerT.EnterField(s)
	}
}

func (s *FieldContext) ExitRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(CsvListener); ok {
		listenerT.ExitField(s)
	}
}

func (p *CsvParser) Field() (localctx IFieldContext) {
	localctx = NewFieldContext(p, p.GetParserRuleContext(), p.GetState())
	p.EnterRule(localctx, 6, CsvParserRULE_field)
	p.SetState(32)
	p.GetErrorHandler().Sync(p)
	if p.HasError() {
		goto errorExit
	}

	switch p.GetTokenStream().LA(1) {
	case CsvParserTEXT:
		p.EnterOuterAlt(localctx, 1)
		{
			p.SetState(29)
			p.Match(CsvParserTEXT)
			if p.HasError() {
				// Recognition error - abort rule
				goto errorExit
			}
		}

	case CsvParserSTRING:
		p.EnterOuterAlt(localctx, 2)
		{
			p.SetState(30)
			p.Match(CsvParserSTRING)
			if p.HasError() {
				// Recognition error - abort rule
				goto errorExit
			}
		}

	case CsvParserT__0, CsvParserT__1, CsvParserT__2:
		p.EnterOuterAlt(localctx, 3)

	default:
		p.SetError(antlr.NewNoViableAltException(p, nil, nil, nil, nil, nil))
		goto errorExit
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
