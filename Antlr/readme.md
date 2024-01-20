# ANTLR

## Setup

To install Java on a Chromebook:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install default-jre
```

Download Antlr:

```bash
wget https://www.antlr.org/download/antlr-4.13.1-complete.jar
```

Check it works:

```bash
java -jar antlr-4.13.1-complete.jar
```

## Notes

* Tokens -- terminal symbols (literal characters)
* Rules -- non-terminal states made up of tokens and/or rules
* Must be saved in a file with the same name as the grammar

* ANTLR converts grammars to parsers automatically
    * Program that writes other programs
* **Grammar** defines the syntax rules of the language
* **Interpreter** computes or executes sentences
* **Parser** (or syntax analyser) recognises a language
    - ANTLR generates recursive-descent parsers
    - resolves ambiguities by choosing the first alternative
* **Lexical analysis** -- groups characters into words or symbols (tokens)
* **Lexer** -- tokenises the input
* **Token** -- consists of:
    - token type
    - text matched for the token
* **Parse tree** or **syntax tree** -- data structure built by the parser
* **Parse-tree listener**
    - responds to events triggered by the tree walker

Generated files consist of three main components:
* Lexer -- returns a stream of tokens
* Parser -- uses the lexer's output to build higher-level structures
* Listener -- Enter and exit functions for each rule in the grammar

* Files automatically created by ANTLR for a given grammar:
    - `<grammar>_base_listener.go` -- set of empty default listener implementations
    - `<grammar>.interp`
    - `<grammar>_lexer.go` -- contains the lexer
    - `<grammar>Lexer.interp`
    - `<grammar>Lexer.tokens`
    - `<grammar>_listener.go` -- defines the listener interface
    - `<grammar>_parser.go` -- contains the parser struct specific to the grammar and a method for each rule
    - `<grammar>.tokens` -- assigns a token type number to each token

### Grammar

* A grammar is a et of the rules that describe the language syntax
* `grammar <name>` -- filename must be `<name>.g4`
* Parser rules start with lowercase letters
* Lexer rules starts with uppercase letters
* `|` separates alternatives of a rule
* `(|)` group symbols with parentheses into subrules, e.g. `('*'|'/')`
* `-> skip` operation is a directive for the lexer to match but throw out whitespace
* To separate the lexer and parser grammar:
    - use `lexer grammar <name>;`
    - `import <name>` to import the lexer grammar
* Labels start `#`-- used to label alternatives in a rule (without labels ANTLR only generates one visitor method per rule)
* Abstract computer language patterns:
    - **Sequence** -- e.g. values in an array initialiser
    - **Choice** -- choice between multiple alternative phrases
    - **Token dependence** -- e.g. left and right parentheses, e.g. `vector : '[' INT+ ']' ;` to match `[1]` or `[1 2]`
    - **Nested phrase** -- self-similar language construct, e.g. nested arithmetic expressions or nested statement blocks
* Sub-rules:
    - `?` optional (zero or one)
    - `*` zero or more
    - `+` one or more
* String literals can be entered directly into the grammar, e.g. `retr : 'RETR' INT '\n' ;`
* Comma-separated list of expressions, such as in a function call: `exprList : expr (',' expr)* ;`
* `|` represents choice, e.g. `field : INT | STRING ;`
* Parse tree
    - internal nodes are rule references
    - leaf nodes are token references
* For right associative: `expr : expr '^'<assoc=right> expr | INT ;`
* `ID : [a-zA-Z]+ ;`
* `INT : [0-9]+ ;`  can also be written `INT : '0'..'9'+ ;`
* `fragment` denotes that a rule will only be used by other lexical rules, e.g.

```
FLOAT : DIGIT+ '.' DIGIT*  // match 1.2
      |        '.' DIGIT+  // match .1
      ;

fragment
DIGIT : [0-9]+ ; // match a single digit
```

* To match a single between double quotes: `STRING : '"' .*? '"' ;`. Note the use of the non-greedy dot wildcard.
* To support common escape characters:

```
STRING : '"' ( ESC | . )*? '"' ;

fragment
ESC : '\\' [btnr"\\] ; // \b, \t, \n etc...
```
* To match comments, but throw them out:

```
LINE_COMMENT : '//' .*? '\r'? '\n' -> skip ; // Match "//" stuff '\n'
COMMENT : '/*' .*? '*/' -> skip ; // Match "/*" stuff "*/"
```

* To match whitespace, but throw out:

```
WS : [ \t\r\n]+ -> skip ; // match 1-or-more whitespace but discard
```

* To match identifiers:

```
ID : ID_LETTER (ID_LETTER | DIGIT)* ; // From C language
fragment ID_LETTER : 'a'..'z'|'A'..'Z'|'_' ;
fragment DIGIT : '0'..'9' ;
```

## Hello, World! example

```bash
cd hello-world
go mod init github.com/cdclaxton/hello-world
go get github.com/antlr4-go/antlr/v4
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser Hello.g4
```

## ArrayInit example

```bash
cd array-init
go mod init github.com/cdclaxton/array-init
go get github.com/antlr4-go/antlr/v4
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser ArrayInit.g4
```

## Expr example

```bash
cd expr
go mod init github.com/cdclaxton/expr
go get github.com/antlr4-go/antlr/v4
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser Expr.g4
```

## CSV example

```bash
cd csv
go mod init github.com/cdclaxton/csv
go get github.com/antlr4-go/antlr/v4
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser Csv.g4
```

## Cymbol function call graph

```bash
cd cymbol-call-graph
go mod init github.com/cdclaxton/cymbol-call-graph
go get github.com/antlr4-go/antlr/v4
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser Cymbol.g4
go run main.go
```

## Validating program symbol usage

```bash
mkdir validate-symbol-usage
cd validate-symbol-usage/
go mod init github.com/cdclaxton/validate-symbol-usage
go get github.com/antlr4-go/antlr/v4
cp ../cymbol-call-graph/Cymbol.g4 .
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser Cymbol.g4
```

## Calculator example

```bash
cd calculator
go mod init github.com/cdclaxton/calculator
go get github.com/antlr4-go/antlr/v4
java -jar ../antlr-4.13.1-complete.jar -Dlanguage=Go -o parser Calc.g4
```

```bash
go run main.go 

# NUMBER ("1")
# ADD ("+")
# NUMBER ("2")
# MUL ("*")
# NUMBER ("3")
# Result: 7
```

## Debugging

To solve:

```
./main.go:20:31: cannot use is (variable of type *antlr.InputStream) as antlr.TokenStream value in argument to parser.NewCsvParser: *antlr.InputStream does not implement antlr.TokenStream (missing method Get)
```

use the lexer and not the parser.