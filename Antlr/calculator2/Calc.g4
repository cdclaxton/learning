grammar Calc;

// Parser rules
expr : term (op=('+' | '-') term)* ;
term : factor (op=('*' | '/') factor)* ;
factor : NUMBER              # Number
       | '(' expr ')'        # Expression
       | ('-' | '+') factor  # UnaryFactor
       ;

// Lexer rules
ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
NUMBER : [0-9]+ ('.' [0-9]+)? ;
WS : [ \t\r\n]+ -> skip ;
