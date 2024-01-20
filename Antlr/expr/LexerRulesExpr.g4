lexer grammar LexerRulesExpr;

ID : [a-zA-Z]+ ;       // identifier
INT : [0-9]+ ;         // integers
NEWLINE : '\r'? '\n' ; // newlines (end of statement signal)
WS : [ \t]+ -> skip ;  // ignore whitespace

MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;
