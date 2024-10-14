grammar ProbabilityDistributions;

// The start rule (begin parsing here)
prog : stat+ ;

// Statement
stat : ID '=' expr NEWLINE   # assign
     | NEWLINE               # blank
     ;

// Expression
expr : expr (op=('*'|'/')) expr    # MulDiv
     | expr (op=('+'|'-')) expr    # AddSub
     | dist                        # exprDist
     | ID                          # id
     ; 

dist : '{' element (',' element)* '}' ;

element : INT ':' FLOAT ;

// Lexer rules
ID : [a-zA-Z]+ ;                   // identifier
INT : [0-9]+ ;                     // integers
FLOAT : [0-9]+ ('.' [0-9]*)?  ;    // float
NEWLINE : '\r'? '\n' ;             // newlines (end of statement signal)
WS : [ \t]+ -> skip ;              // ignore whitespace

MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;
