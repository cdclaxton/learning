grammar Expr;

// The start rule (begin parsing here)
prog : stat+ ;

// Statement
stat : ID '=' expr NEWLINE   # assign
     | NEWLINE               # blank
     ;

// Expression
 expr : expr (op=('*'|'/')) expr   # MulDiv
      | expr (op=('+'|'-')) expr   # AddSub
      | INT                        # int 
      | ID                         # id
      | '(' expr ')'               # parens
      ;

// Lexer rules
ID : [a-zA-Z]+ ;       // identifier
INT : [0-9]+ ;         // integers
NEWLINE : '\r'? '\n' ; // newlines (end of statement signal)
WS : [ \t]+ -> skip ;  // ignore whitespace

MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;
