package main

import (
	"fmt"
	"strings"

	"github.com/antlr4-go/antlr/v4"
	"github.com/cdclaxton/cymbol-call-graph/parser"
)

type Graph struct {
	// Set of nodes
	nodes map[string]bool

	// Source to destination
	edges map[string]map[string]bool
}

func NewGraph() *Graph {
	return &Graph{
		nodes: map[string]bool{},
		edges: map[string]map[string]bool{},
	}
}

func (g *Graph) AddNode(node string) {
	g.nodes[node] = true
}

func (g *Graph) AddEdge(source, target string) {
	_, ok := g.edges[source]
	if !ok {
		g.edges[source] = map[string]bool{}
	}

	g.edges[source][target] = true
}

func (g *Graph) ToDot() string {
	var buffer strings.Builder

	buffer.WriteString("digraph G {\n")
	buffer.WriteString(" ranksep=.25;\n")
	buffer.WriteString(" edge [arrowsize=.5]\n")
	buffer.WriteString(" node [shape=circle, fontname=\"ArialNarrow\",\n")
	buffer.WriteString(" fontsize=12, fixedsize=true, height=.45];\n")
	buffer.WriteString(" ")

	// List all nodes
	for node := range g.nodes {
		buffer.WriteString(node)
		buffer.WriteString(";")
	}

	buffer.WriteString("\n")

	// List the edges
	for src := range g.edges {
		for target := range g.edges[src] {
			buffer.WriteString(" ")
			buffer.WriteString(src)
			buffer.WriteString(" -> ")
			buffer.WriteString(target)
			buffer.WriteString(";\n")
		}
	}

	buffer.WriteString("}\n")

	return buffer.String()
}

type CallGraphListener struct {
	parser.BaseCymbolListener
	graph               *Graph
	currentFunctionName string
}

func NewCallGraphListener() *CallGraphListener {
	return &CallGraphListener{
		graph: NewGraph(),
	}
}

func (c *CallGraphListener) EnterFunctionDecl(ctx *parser.FunctionDeclContext) {
	c.currentFunctionName = ctx.ID().GetText()
	c.graph.AddNode(c.currentFunctionName)
}

func (c *CallGraphListener) ExitCall(ctx *parser.CallContext) {
	funcName := ctx.ID().GetText()
	c.graph.AddEdge(c.currentFunctionName, funcName)
}

func main() {
	program := `

int main() { fact(); a(); }

float fact(int n) {
	print(n);
	if ( n==0 ) then return 1;
	return n * fact(n-1);
}

void a() { int x = b(); if false then {c(); d();} }
void b() { c(); }
void c() { b(); }
void d() { }
void e() { }
`

	is := antlr.NewInputStream(program)

	// Create the lexer
	lexer := parser.NewCymbolLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)

	// Create the parser
	p := parser.NewCymbolParser(stream)

	// Create the listener
	listener := NewCallGraphListener()
	antlr.ParseTreeWalkerDefault.Walk(listener, p.File())

	fmt.Println(listener.graph.ToDot())
}
